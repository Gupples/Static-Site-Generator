import unittest
from inline_markdown import split_nodes_delimiter
from textnode import TextType, TextNode

class TestDelimiterSplit(unittest.TestCase):
    def test_split_nodes_delimiter_pure_text(self):
        node = TextNode("This is a text node", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "`", TextType.CODE)
        expected = [TextNode("This is a text node", TextType.TEXT)]
        self.assertEqual(len(new_nodes), 1)
        self.assertEqual(new_nodes, expected)
    
    def test_split_nodes_delimiter_pure_code(self):
        node = TextNode("This is a code block", TextType.CODE)
        new_nodes = split_nodes_delimiter([node], "`", TextType.CODE)
        expected = [TextNode("This is a code block", TextType.CODE)]
        self.assertEqual(len(new_nodes), 1)
        self.assertEqual(new_nodes, expected)

    def test_split_nodes_delimiter_code_block(self):
        node = TextNode("This is text with a `code block` word", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "`", TextType.CODE)
        expected = [
            TextNode("This is text with a ", TextType.TEXT),
            TextNode("code block", TextType.CODE),
            TextNode(" word", TextType.TEXT),
            ]
        self.assertEqual(len(new_nodes), 3)
        self.assertEqual(new_nodes, expected)

    def test_split_nodes_delimiter_bold_block(self):
        node = TextNode("This is text with a **bold block** word", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
        expected = [
            TextNode("This is text with a ", TextType.TEXT),
            TextNode("bold block", TextType.BOLD),
            TextNode(" word", TextType.TEXT),
            ]
        self.assertEqual(len(new_nodes), 3)
        self.assertEqual(new_nodes, expected)

    def test_split_nodes_delimiter_italic_block(self):
        node = TextNode("This is text with a _italic block_ word", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "_", TextType.ITALIC)
        expected = [
            TextNode("This is text with a ", TextType.TEXT),
            TextNode("italic block", TextType.ITALIC),
            TextNode(" word", TextType.TEXT),
            ]
        self.assertEqual(len(new_nodes), 3)
        self.assertEqual(new_nodes, expected)

    # ERRORS
    def test_split_nodes_delimiter_uneven_code(self):
        with self.assertRaises(Exception) as e:
            node = TextNode("This is an invalid `code block", TextType.TEXT)
            new_nodes = split_nodes_delimiter([node], "`", TextType.CODE)
            print(new_nodes)
        self.assertEqual(str(e.exception), "Invalid Markdown; no closing delimiter")