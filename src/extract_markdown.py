import re

def extract_markdown_images(text):
    image_pattern = r"!\[([^\[\]]*)\]\(([^\(\)]*)\)"
    return re.findall(image_pattern, text)

def extract_markdown_links(text):
    link_pattern = r"(?<!!)\[([^\[\]]*)\]\(([^\(\)]*)\)"
    return re.findall(link_pattern, text)

def markdown_to_blocks(markdown):
    full_text = markdown.split("\n\n")
    filtered_blocks = []
    for text in full_text:
        if text == "":
            continue
        filtered_blocks.append(text.strip())

    return filtered_blocks

def extract_title(markdown):
    title_pattern = r"^#+\s*(.*)$"
    titles = re.findall(title_pattern, markdown, re.MULTILINE)
    if not titles:
        raise ValueError("No titles found in the markdown content.")
    return titles

# Backwards-compat alias for tests expecting extract_titles
def extract_titles(markdown):
    return extract_title(markdown)
