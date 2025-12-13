from textnode import TextNode, TextType
from htmlnode import LeafNode, ParentNode

def main():
    node = TextNode("This is a text node", TextType.BOLD, "https://www.boot.dev")
    html_node = LeafNode("a", node.text, {"href": node.url})
    parent_node = ParentNode(
    "p",
    [
        LeafNode("b", "Bold text"),
        LeafNode(None, "Normal text"),
        LeafNode("i", "italic text"),
        LeafNode(None, "Normal text"),
    ],
)
    print(parent_node.to_html())

if __name__ == "__main__":
    main()