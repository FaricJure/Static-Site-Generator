import os
import shutil

from extract_markdown import extract_title
from markdown_to_html import markdown_to_html_node



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
    print("Writing the new full HTML page to the destination directory.")
    generate_page(
        from_path="content/index.md",
        template_path="template.html",
        dest_path="public/index.html",
    )

def generate_page(from_path, template_path, dest_path):
    print(f"Generating page from {from_path} to {dest_path} using {template_path}")
    with open(from_path, "r", encoding="utf-8") as f:
        from_path_content = f.read()
    with open(template_path, "r", encoding="utf-8") as f:
        template_content = f.read()

    html_content = markdown_to_html_node(from_path_content)
    final_content = html_content.to_html()

    page_title = extract_title(from_path_content)[0]
    final_page = template_content.replace("{{ Content }}", final_content).replace("{{ Title }}", page_title)

    with open(dest_path, "w", encoding="utf-8") as f:
        f.write(final_page)

def main():
    clear_directory()


if __name__ == "__main__":
    main()
