import os
import shutil


def _remove_recursive(path: str) -> None:
    """Recursively delete files/directories at path (similar to shutil.rmtree)."""
    if os.path.isdir(path) and not os.path.islink(path):
        for entry in os.scandir(path):
            _remove_recursive(entry.path)
        os.rmdir(path)
    else:
        os.remove(path)


def clear_directory(dst: str = "public", src: str = "static") -> None:
    if os.path.exists(dst):
        print(f"Clearing directory: {dst}")
        _remove_recursive(dst)
    else:
        print(f"Directory does not exist: {dst}")

    print(f"Creating directory: {dst}")
    os.makedirs(dst, exist_ok=True)
    print(f"Copying static files to: {dst}")
    shutil.copytree(src, dst, dirs_exist_ok=True)


def main():
    clear_directory()


if __name__ == "__main__":
    main()
