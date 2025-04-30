import glob
import os
import platform
import shutil
import subprocess

from setuptools import Extension, setup
from setuptools.command.build_ext import build_ext

try:
    from setuptools.command.bdist_wheel import bdist_wheel as _bdist_wheel
except ModuleNotFoundError:
    from wheel.bdist_wheel import bdist_wheel as _bdist_wheel


class CMakeExtension(Extension):
    def __init__(self, name):
        # Don't invoke the original build_ext for this special extension
        super().__init__(name, sources=[])


class CMakeBuild(build_ext):
    def run(self):
        for ext in self.extensions:
            self.build_cmake(ext)

    def build_cmake(self, ext):
        # Get CMAKE_ARGS from environment
        cmake_args = os.environ.get("CMAKE_ARGS", "").split()

        # Create build directory
        build_dir = os.path.abspath("build")
        os.makedirs(build_dir, exist_ok=True)

        # Get submodule path
        llama_cpp_dir = os.path.abspath("llama.cpp")

        # Add RPATH settings based on the platform
        system = platform.system()
        if system == "Linux":
            cmake_args.extend([
                "-DCMAKE_INSTALL_RPATH=$ORIGIN",
                "-DCMAKE_BUILD_WITH_INSTALL_RPATH=ON",
                "-DCMAKE_INSTALL_RPATH_USE_LINK_PATH=OFF"
            ])
        elif system == "Darwin":  # macOS
            cmake_args.extend([
                "-DCMAKE_INSTALL_RPATH=@executable_path",
                "-DCMAKE_BUILD_WITH_INSTALL_RPATH=ON",
                "-DCMAKE_INSTALL_RPATH_USE_LINK_PATH=OFF"
            ])

        # Disable Curl
        cmake_args.append("-DLLAMA_CURL=OFF")

        # Configure with CMake
        cmake_cmd = ["cmake", llama_cpp_dir] + cmake_args
        subprocess.check_call(cmake_cmd, cwd=build_dir)

        # Build with multiple cores
        jobs = os.environ.get("LLAMA_CPP_BUILD_JOBS", "")
        build_cmd = ["cmake", "--build", ".", "--config", "Release", "-j" + jobs]
        subprocess.check_call(build_cmd, cwd=build_dir)

        # Copy all files from bin directory to package
        bin_dir = os.path.join(build_dir, "bin")
        llama_dir = next((d for d in os.listdir(self.build_lib) if d.startswith("llama_cpp_binaries") and os.path.isdir(os.path.join(self.build_lib, d))), "llama_cpp_binaries")
        target_dir = os.path.join(self.build_lib, llama_dir, "bin")
        os.makedirs(target_dir, exist_ok=True)

        # Check for Windows-style Release subdirectory
        if os.path.exists(os.path.join(bin_dir, "Release")):
            bin_dir = os.path.join(bin_dir, "Release")

        for file in glob.glob(os.path.join(bin_dir, "*")):
            shutil.copy(file, target_dir)


class UniversalBdistWheel(_bdist_wheel):
    def finalize_options(self):
        super().finalize_options()
        # Mark as non-pure even if no extensions
        self.root_is_pure = False  # Critical for platform tags

    def get_tag(self):
        python, abi, plat = super().get_tag()
        # Force Python 3 and no ABI requirement
        return ('py3', 'none', plat)


setup(
    ext_modules=[CMakeExtension("llama_cpp_binaries")],
    cmdclass={
        'build_ext': CMakeBuild,
        'bdist_wheel': UniversalBdistWheel
    },
)
