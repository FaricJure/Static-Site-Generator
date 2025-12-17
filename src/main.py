import os
import re
import shutil
import sys

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


def clear_directory(dst: str = "docs", src: str = "static") -> None:
    if os.path.exists(dst):
        print(f"Clearing directory: {dst}")
        _remove_recursive(dst)
    else:
        print(f"Directory does not exist: {dst}")

    print(f"Creating directory: {dst}")
    os.makedirs(dst, exist_ok=True)
    print(f"Copying static files to: {dst}")
    shutil.copytree(src, dst, dirs_exist_ok=True)

def generate_page(from_path, template_path, dest_path, basepath):
    print(f"Generating page from {from_path} to {dest_path} using {template_path}")
    with open(from_path, "r", encoding="utf-8") as f:
        from_path_content = f.read()
    with open(template_path, "r", encoding="utf-8") as f:
        template_content = f.read()

    html_content = markdown_to_html_node(from_path_content)
    final_content = html_content.to_html()

    page_title = extract_title(from_path_content)[0]
    final_page = template_content.replace("{{ Content }}", final_content).replace("{{ Title }}", page_title)
    
    def apply_basepath(html: str, base: str) -> str:
        if base in ("", "/"):
            prefix = ""
        else:
            prefix = "/" + base.strip("/")

        def repl_href(match):
            path = match.group(1)
            return f'href="{prefix + "/" + path if prefix else "/" + path}"'

        def repl_src(match):
            path = match.group(1)
            return f'src="{prefix + "/" + path if prefix else "/" + path}"'

        html = re.sub(r'href="/([^"]*)"', repl_href, html)
        html = re.sub(r'src="/([^"]*)"', repl_src, html)
        return html

    final_page = apply_basepath(final_page, basepath)

    with open(dest_path, "w", encoding="utf-8") as f:
        f.write(final_page)

def generate_pages_recursive(dir_path_content, template_path, dest_dir_path, basepath):
    for entry in os.scandir(dir_path_content):
        if entry.is_file() and entry.name.endswith(".md"):
            relative_path = os.path.relpath(entry.path, dir_path_content)
            dest_path = os.path.join(dest_dir_path, relative_path[:-3] + ".html")
            os.makedirs(os.path.dirname(dest_path), exist_ok=True)
            generate_page(entry.path, template_path, dest_path, basepath)

        elif entry.is_dir():
            new_dest_dir = os.path.join(dest_dir_path, entry.name)
            os.makedirs(new_dest_dir, exist_ok=True)
            generate_pages_recursive(entry.path, template_path, new_dest_dir, basepath)

def main():
    basepath = sys.argv[1] if len(sys.argv) > 1 else "/"
    clear_directory()
    print("Writing the new full HTML page to the destination directory.")
    generate_pages_recursive(
        dir_path_content="content",
        template_path="template.html",
        dest_dir_path="docs",
        basepath=basepath,
    )


if __name__ == "__main__":
    main()
