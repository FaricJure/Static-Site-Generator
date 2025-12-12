from textnode import TextNode, TextType
from htmlnode import LeafNode

def main():
    node = TextNode("This is a text node", TextType.BOLD, "https://www.boot.dev")
    html_node = LeafNode("a", node.text, {"href": node.url})
    print(html_node.to_html())

if __name__ == "__main__":
    main()