import unittest

from textnode import TextNode, TextType,text_node_to_html_node
from htmlnode import HTMLNode, LeafNode, ParentNode
from extractLinks import extract_markdown_images
from splitImages import split_nodes_image
class TestTextNode(unittest.TestCase):
    def test_eq(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.BOLD)
        self.assertEqual(node, node2)
    def test_props_to_html(self):
        node = HTMLNode("a", "link", None, {"href": "https://www.boot.dev"})
        self.assertEqual(node.props_to_html(), ' href="https://www.boot.dev"')
    def test_props_none(self):
        node = HTMLNode("a", "link",None,None)
        self.assertEqual(node.props_to_html(), "")
    def test_props_empty(self):
        node = HTMLNode("a", "link",None,{})
        self.assertEqual(node.props_to_html(), "")
    def test_muiltiple_props(self):
        node = HTMLNode("a", "link", None, {"href": "https://www.boot.dev", "target": "https://www.google.com"})
        self.assertEqual(node.props_to_html(), ' href="https://www.boot.dev" target="https://www.google.com"')
    def test_leaf_to_html_p(self):
        node = LeafNode("p", "Hello, world!")
        self.assertEqual(node.to_html(), "<p>Hello, world!</p>")
    def test_leaf_with_odd_tag(self):
        node = LeafNode("a", "Hello, world!")
        self.assertEqual(node.to_html(), "<a>Hello, world!</a>")
    def test_leaf_with_prop(self):
        node = LeafNode("a", "Hello, world!",{"href": "https://www.boot.dev", "target": "https://www.google.com"})
        self.assertEqual(node.to_html(), '<a href="https://www.boot.dev" target="https://www.google.com">Hello, world!</a>')
    def test_leaf_cannot_have_children(self):
        node = LeafNode("p", "Hello")
        with self.assertRaises(ValueError):
            node.children = [LeafNode("span", "nope")]
    def test_leaf_missing_value_raises(self):
        node = LeafNode("p", None)
        with self.assertRaises(ValueError):
            node.to_html()
    def test_leaf_no_tag_returns_value(self):
        node = LeafNode(None, "Just text")
        self.assertEqual(node.to_html(), "Just text")
    def test_to_html_with_children(self):
        child_node = LeafNode("span", "child")
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(parent_node.to_html(), "<div><span>child</span></div>")
    def test_to_html_with_grandchildren(self):
        grandchild_node = LeafNode("b", "grandchild")
        child_node = ParentNode("span", [grandchild_node])
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(
            parent_node.to_html(),
            "<div><span><b>grandchild</b></span></div>",
        )
    def test_text(self):
        node = TextNode("This is a text node", TextType.TEXT)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, None)
        self.assertEqual(html_node.value, "This is a text node")
    def test_extract_markdown_images(self):
        matches = extract_markdown_images(
        "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png)"
    )
        self.assertListEqual([("image", "https://i.imgur.com/zjjcJKZ.png")], matches)
    def test_split_images(self):
        node = TextNode(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and another ![second image](https://i.imgur.com/3elNhQu.png)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("This is text with an ", TextType.TEXT),
                TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(" and another ", TextType.TEXT),
                TextNode(
                    "second image", TextType.IMAGE, "https://i.imgur.com/3elNhQu.png"
                ),
            ],
            new_nodes,
        )

if __name__ == "__main__":
    unittest.main()