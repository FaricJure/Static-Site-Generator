from enum import Enum

class BlockType(Enum):
    PARAGRAPH = "paragraph"
    HEADING = "heading"
    CODE = "code"
    QUOTE = "quote"
    UNORDERED_LIST = "unordered_list"
    ORDERED_LIST = "ordered_list"

def block_to_block_type(block):
    stripped = block.strip()
    if stripped.startswith(("# ", "## ", "### ", "#### ", "##### ", "###### ")):
        return BlockType.HEADING
    if stripped.startswith("```") and stripped.endswith("```"):
        return BlockType.CODE
    if stripped.startswith(">"):
        return BlockType.QUOTE
    if stripped.startswith("- "):
        return BlockType.UNORDERED_LIST
    if any(stripped.startswith(f"{i}. ") for i in range(1, 10)):
        return BlockType.ORDERED_LIST
    return BlockType.PARAGRAPH