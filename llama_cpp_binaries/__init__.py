import os
import platform

def get_binary_path():
    """Return the path to the appropriate llama-server binary"""
    system = platform.system()
    if system == "Windows":
        executable = "llama-server.exe"
    else:
        executable = "llama-server"

    # Get the package directory
    package_dir = os.path.dirname(os.path.abspath(__file__))
    bin_dir = os.path.join(package_dir, "bin")
    return os.path.join(bin_dir, executable)
