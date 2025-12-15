from textnode import TextNode, TextType, split_nodes_image, split_nodes_link, text_to_textnodes
from htmlnode import LeafNode, ParentNode
#from split_nodes import split_nodes_delimiter

def main():
    # node = TextNode("This is a text node", TextType.BOLD, "https://www.boot.dev")
    node = TextNode("This is **text** with an _italic_ word and a `code block` and an ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) and a [link](https://boot.dev)", TextType.TEXT)
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
    """
    node_to_split = TextNode("This is text with a `code block` word", TextType.TEXT)
    split_nodes = split_nodes_delimiter(node_to_split, "`", TextType.CODE)
    print("Split Nodes:")
    for sn in split_nodes:
        print(sn)
    #print(parent_node.to_html())
    """
    """
    new_nodes = split_nodes_link([node])
    for nn in new_nodes:
        print(nn)
    """
    text_to_textnodes(node.text)
    print(text_to_textnodes(node.text))

if __name__ == "__main__":
    main()