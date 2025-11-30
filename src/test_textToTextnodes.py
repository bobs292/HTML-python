import unittest
from textToTextnodes import text_to_textnodes
from textnode import TextNode, TextType
from blocktypes import markdown_to_html_node
class TestTextToTextnodes(unittest.TestCase):

    def test_plain_text(self):
        """Test with plain text only"""
        text = "This is just plain text"
        result = text_to_textnodes(text)
        expected = [TextNode("This is just plain text", TextType.TEXT)]
        self.assertEqual(result, expected)

    def test_bold_text(self):
        """Test with bold formatting"""
        text = "This is **bold** text"
        result = text_to_textnodes(text)
        expected = [
            TextNode("This is ", TextType.TEXT),
            TextNode("bold", TextType.BOLD),
            TextNode(" text", TextType.TEXT)
        ]
        self.assertEqual(result, expected)

    def test_italic_text(self):
        """Test with italic formatting"""
        text = "This is _italic_ text"
        result = text_to_textnodes(text)
        expected = [
            TextNode("This is ", TextType.TEXT),
            TextNode("italic", TextType.ITALIC),
            TextNode(" text", TextType.TEXT)
        ]
        self.assertEqual(result, expected)

    def test_code_text(self):
        """Test with code formatting"""
        text = "This is `code` text"
        result = text_to_textnodes(text)
        expected = [
            TextNode("This is ", TextType.TEXT),
            TextNode("code", TextType.CODE),
            TextNode(" text", TextType.TEXT)
        ]
        self.assertEqual(result, expected)

    def test_multiple_formatting(self):
        """Test with multiple formatting types"""
        text = "This is **bold** and _italic_ and `code` text"
        result = text_to_textnodes(text)
        expected = [
            TextNode("This is ", TextType.TEXT),
            TextNode("bold", TextType.BOLD),
            TextNode(" and ", TextType.TEXT),
            TextNode("italic", TextType.ITALIC),
            TextNode(" and ", TextType.TEXT),
            TextNode("code", TextType.CODE),
            TextNode(" text", TextType.TEXT)
        ]
        self.assertEqual(result, expected)

    def test_nested_formatting(self):
        """Test with nested formatting (should not be nested, outer takes precedence)"""
        text = "This is **bold with _italic_ inside** text"
        result = text_to_textnodes(text)
        expected = [
            TextNode("This is ", TextType.TEXT),
            TextNode("bold with _italic_ inside", TextType.BOLD),
            TextNode(" text", TextType.TEXT)
        ]
        self.assertEqual(result, expected)

    def test_image_markdown(self):
        """Test with image markdown"""
        text = "This is text with an ![image](https://example.com/image.png) in it"
        result = text_to_textnodes(text)
        expected = [
            TextNode("This is text with an ", TextType.TEXT),
            TextNode("image", TextType.IMAGE, "https://example.com/image.png"),
            TextNode(" in it", TextType.TEXT)
        ]
        self.assertEqual(result, expected)

    def test_link_markdown(self):
        """Test with link markdown"""
        text = "This is text with a [link](https://example.com) in it"
        result = text_to_textnodes(text)
        expected = [
            TextNode("This is text with a ", TextType.TEXT),
            TextNode("link", TextType.LINK, "https://example.com"),
            TextNode(" in it", TextType.TEXT)
        ]
        self.assertEqual(result, expected)

    def test_multiple_images_and_links(self):
        """Test with multiple images and links"""
        text = "![image1](https://example.com/img1.png) and [link1](https://example.com) and ![image2](https://example.com/img2.png)"
        result = text_to_textnodes(text)
        expected = [
            TextNode("image1", TextType.IMAGE, "https://example.com/img1.png"),
            TextNode(" and ", TextType.TEXT),
            TextNode("link1", TextType.LINK, "https://example.com"),
            TextNode(" and ", TextType.TEXT),
            TextNode("image2", TextType.IMAGE, "https://example.com/img2.png")
        ]
        self.assertEqual(result, expected)

    def test_complex_mixed_formatting(self):
        """Test with complex mixed formatting"""
        text = "This **bold** text has `code` and _italic_ and ![image](https://example.com/img.png) and [link](https://example.com)"
        result = text_to_textnodes(text)
        expected = [
            TextNode("This ", TextType.TEXT),
            TextNode("bold", TextType.BOLD),
            TextNode(" text has ", TextType.TEXT),
            TextNode("code", TextType.CODE),
            TextNode(" and ", TextType.TEXT),
            TextNode("italic", TextType.ITALIC),
            TextNode(" and ", TextType.TEXT),
            TextNode("image", TextType.IMAGE, "https://example.com/img.png"),
            TextNode(" and ", TextType.TEXT),
            TextNode("link", TextType.LINK, "https://example.com")
        ]
        self.assertEqual(result, expected)

    def test_empty_string(self):
        """Test with empty string"""
        text = ""
        result = text_to_textnodes(text)
        expected = []  # Empty strings are filtered out
        self.assertEqual(result, expected)

    def test_only_formatting(self):
        """Test with only formatting, no plain text"""
        text = "**bold**"
        result = text_to_textnodes(text)
        expected = [TextNode("bold", TextType.BOLD)]
        self.assertEqual(result, expected)

    def test_consecutive_formatting(self):
        """Test with consecutive formatting"""
        text = "**bold**_italic_`code`"
        result = text_to_textnodes(text)
        expected = [
            TextNode("bold", TextType.BOLD),
            TextNode("italic", TextType.ITALIC),
            TextNode("code", TextType.CODE)
        ]
        self.assertEqual(result, expected)

    def test_formatting_at_edges(self):
        """Test with formatting at the beginning and end"""
        text = "**start** middle _end_"
        result = text_to_textnodes(text)
        expected = [
            TextNode("start", TextType.BOLD),
            TextNode(" middle ", TextType.TEXT),
            TextNode("end", TextType.ITALIC)
        ]
        self.assertEqual(result, expected)

    def test_unclosed_formatting_raises_exception(self):
        """Test that unclosed formatting raises an exception"""
        text = "This has **unclosed bold formatting"
        with self.assertRaises(Exception) as context:
            text_to_textnodes(text)
        self.assertIn("invalid markdown, formatted section not closed", str(context.exception))

    def test_paragraphs(self):
        md = """
    This is **bolded** paragraph
    text in a p
    tag here

    This is another paragraph with _italic_ text and `code` here

    """

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><p>This is <b>bolded</b> paragraph text in a p tag here</p><p>This is another paragraph with <i>italic</i> text and <code>code</code> here</p></div>",
        )

    def test_codeblock(self):
        md = """
    ```
    This is text that _should_ remain
    the **same** even with inline stuff
    ```
    """

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><pre><code>This is text that _should_ remain\nthe **same** even with inline stuff\n</code></pre></div>",
        ) 
if __name__ == '__main__':
    unittest.main()