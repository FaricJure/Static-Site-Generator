import textwrap
from block import block_to_block_type, BlockType
from extract_markdown import markdown_to_blocks
from htmlnode import HTMLNode, LeafNode, ParentNode
from textnode import text_node_to_html_node, text_to_textnodes


def inline_to_html(text: str) -> str:
    nodes = text_to_textnodes(text)
    html_parts = [text_node_to_html_node(n).to_html() for n in nodes]
    return "".join(html_parts)


def paragraph_to_html(block: str) -> HTMLNode:
    cleaned = " ".join(line.strip() for line in block.splitlines() if line.strip())
    return LeafNode(tag="p", value=inline_to_html(cleaned))


def heading_to_html(block: str) -> HTMLNode:
    level = block.count("#", 0, block.index(" "))
    content = block[level + 1 :].strip()
    return LeafNode(tag=f"h{level}", value=inline_to_html(content))


def codeblock_to_html(block: str) -> HTMLNode:
    lines = block.split("\n")
    if lines and lines[0].strip().startswith("```"):
        lines = lines[1:]
    if lines and lines[-1].strip().startswith("```"):
        lines = lines[:-1]
    code_content = textwrap.dedent("\n".join(lines))
    if not code_content.endswith("\n"):
        code_content += "\n"
    return LeafNode(tag="pre", value=LeafNode(tag="code", value=code_content).to_html())


def quote_to_html(block: str) -> HTMLNode:
    cleaned_lines = []
    for line in block.splitlines():
        stripped = line.lstrip()
        if stripped.startswith(">"):
            stripped = stripped[1:]
        cleaned_lines.append(stripped.strip())
    quote_content = " ".join(l for l in cleaned_lines if l)
    return LeafNode(tag="blockquote", value=inline_to_html(quote_content))


def unordered_list_to_html(block: str) -> HTMLNode:
    items = [item.strip("- ").strip() for item in block.split("\n")]
    list_items = [LeafNode(tag="li", value=inline_to_html(item)) for item in items if item]
    return ParentNode(tag="ul", children=list_items)


def ordered_list_to_html(block: str) -> HTMLNode:
    items = [item[item.index(".") + 1 :].strip() for item in block.split("\n") if item]
    list_items = [LeafNode(tag="li", value=inline_to_html(item)) for item in items]
    return ParentNode(tag="ol", children=list_items)


def markdown_to_html_node(markdown: str) -> HTMLNode:
    blocks = markdown_to_blocks(markdown)
    html_nodes = []

    for block in blocks:
        if not block or not block.strip():
            continue
        block_type = block_to_block_type(block)

        if block_type == BlockType.PARAGRAPH:
            node = paragraph_to_html(block)
        elif block_type == BlockType.HEADING:
            node = heading_to_html(block)
        elif block_type == BlockType.CODE:
            node = codeblock_to_html(block)
        elif block_type == BlockType.QUOTE:
            node = quote_to_html(block)
        elif block_type == BlockType.UNORDERED_LIST:
            node = unordered_list_to_html(block)
        elif block_type == BlockType.ORDERED_LIST:
            node = ordered_list_to_html(block)
        else:
            continue  # Skip unknown block types

        html_nodes.append(node)

    return ParentNode(tag="div", children=html_nodes)
