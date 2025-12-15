from enum import Enum
from htmlnode import LeafNode, ParentNode, HTMLNode
from extract_markdown import extract_markdown_images, extract_markdown_links

class TextType(Enum):
    TEXT = "text"
    BOLD = "bold"
    ITALIC = "italic"
    CODE = "code"
    LINK = "link"
    IMAGE = "image"

class TextNode:
    def __init__(self, text: str, text_type: TextType, url: str = None):
        self.text = text
        self.text_type = text_type
        self.url = url

    def __eq__(self, other) -> bool:
        if not isinstance(other, TextNode):
            return False
        return (
            self.text == other.text
            and self.text_type == other.text_type
            and self.url == other.url
        )

    def __repr__(self) -> str:
        # TextNode(TEXT, TEXT_TYPE, URL)
        if self.url:
            return f"TextNode({self.text}, {self.text_type.value}, {self.url})"
        else:
            return f"TextNode({self.text}, {self.text_type.value})"

def text_node_to_html_node(text_node):
    if text_node.text_type == TextType.TEXT:
        return LeafNode(None, text_node.text)
    if text_node.text_type == TextType.BOLD:
        return LeafNode("b", text_node.text)
    if text_node.text_type == TextType.ITALIC:
        return LeafNode("i", text_node.text)
    if text_node.text_type == TextType.CODE:
        return LeafNode("code", text_node.text)
    if text_node.text_type == TextType.LINK:
        return LeafNode("a", text_node.text, {"href": text_node.url})
    if text_node.text_type == TextType.IMAGE:
        return LeafNode("img", "", {"src": text_node.url, "alt": text_node.text})
    raise ValueError(f"invalid text type: {text_node.text_type}")

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
