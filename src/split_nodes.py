from textnode import TextNode, TextType
import re

def split_nodes_delimiter(old_nodes, delimiter, text_type):
    nodes = old_nodes if isinstance(old_nodes, list) else [old_nodes]
    new_nodes = []
    for node in nodes:
        if node.text_type != TextType.TEXT:
            new_nodes.append(node)
            continue

        if delimiter not in node.text:
            if not isinstance(old_nodes, list):
                raise ValueError("Delimiter not found in text node.")
            new_nodes.append(node)
            continue

        parts = node.text.split(delimiter)
        for i, part in enumerate(parts):
            if not part:
                continue
            if i % 2 == 0:
                new_nodes.append(TextNode(part, TextType.TEXT))
            else:
                new_nodes.append(TextNode(part, text_type))
    return new_nodes

def split_nodes_image(old_nodes):
    from split_nodes import split_nodes_delimiter
    new_nodes = []
    for node in old_nodes:
        images = extract_markdown_images(node.text)
        original_text = node.text
        for alt_text, url in images:
            sections = original_text.split(f"![{alt_text}]({url})", 1)
            if not url:
                continue
            delimiter = f"![{alt_text}]({url})"
            if sections[0]:
                new_nodes.append(TextNode(sections[0], TextType.TEXT))
            new_nodes.append(TextNode(alt_text, TextType.IMAGE, url))
            original_text = sections[1]
        if original_text:
            new_nodes.append(TextNode(original_text, TextType.TEXT))
    return new_nodes
    

def split_nodes_link(old_nodes):
    from split_nodes import split_nodes_delimiter
    new_nodes = []
    for node in old_nodes:
        links = extract_markdown_links(node.text)
        original_text = node.text
        for link_text, url in links:
            sections = original_text.split(f"[{link_text}]({url})", 1)
            if not url:
                continue
            delimiter = f"[{link_text}]({url})"
            if sections[0]:
                new_nodes.append(TextNode(sections[0], TextType.TEXT))
            new_nodes.append(TextNode(link_text, TextType.LINK, url))
            original_text = sections[1]
        if original_text:
            new_nodes.append(TextNode(original_text, TextType.TEXT))
    return new_nodes

def extract_markdown_images(text):
    image_pattern = r"!\[([^\[\]]*)\]\(([^\(\)]*)\)"
    return re.findall(image_pattern, text)

def extract_markdown_links(text):
    link_pattern = r"(?<!!)\[([^\[\]]*)\]\(([^\(\)]*)\)"
    return re.findall(link_pattern, text)