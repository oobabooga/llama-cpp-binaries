import json
import os
import platform


def _restore_symlinks():
    """Restore symlinks from manifest (wheels don't support symlinks natively)."""
    bin_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "bin")
    manifest = os.path.join(bin_dir, "_symlinks.json")

    if not os.path.exists(manifest):
        return

    with open(manifest) as f:
        symlinks = json.load(f)

    for name, target in symlinks.items():
        link = os.path.join(bin_dir, name)

        # 1. Force remove if it exists (link or file)
        if os.path.lexists(link):
            try:
                os.remove(link)
            except OSError:
                pass # Permission error, read-only, etc.

        # 2. Create the new link
        try:
            os.symlink(target, link)
        except OSError:
            pass

    try:
        os.remove(manifest)
    except OSError:
        pass


if platform.system() != "Windows":
    _restore_symlinks()


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
