import unittest
from inline_markdown import split_nodes_delimiter, extract_markdown_images, extract_markdown_links
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

class TestExtractors(unittest.TestCase):
    def test_extract_markdown_images_none(self):
        text = "This string has no image"
        images = extract_markdown_images(text)
        expected = []
        self.assertEqual(len(images), 0)
        self.assertListEqual(images, expected)

    def test_extract_markdown_images_one(self):
        text = "This string has one image; ![rick roll](https://i.imgur.com/aKaOqIh.gif)"
        images = extract_markdown_images(text)
        expected = [("rick roll", "https://i.imgur.com/aKaOqIh.gif")]
        self.assertEqual(len(images), 1)
        self.assertListEqual(images, expected)

    def test_extract_markdown_images_two(self):
        text = "This string has some images; ![rick roll](https://i.imgur.com/aKaOqIh.gif) and ![obi wan](https://i.imgur.com/fJRm4Vk.jpeg)"
        images = extract_markdown_images(text)
        expected = [("rick roll", "https://i.imgur.com/aKaOqIh.gif"),
                     ("obi wan", "https://i.imgur.com/fJRm4Vk.jpeg"),]
        self.assertEqual(len(images), 2)
        self.assertListEqual(images, expected)

    def test_extract_markdown_links_none(self):
        text = "This string has no links"
        links = extract_markdown_links(text)
        expected = []
        self.assertEqual(len(links), 0)
        self.assertListEqual(links, expected)

    def test_extract_markdown_links_one(self):
        text = "This string has a link; [rick roll](https://i.imgur.com/aKaOqIh.gif)"
        links = extract_markdown_links(text)
        expected = [("rick roll", "https://i.imgur.com/aKaOqIh.gif"),]
        self.assertEqual(len(links), 1)
        self.assertListEqual(links, expected)

    def test_extract_markdown_links_some(self):
        text = "This string has some links; [A guide to vigilance](https://youtu.be/dQw4w9WgXcQ?si=_4faL0F6NnUpr9cB) and [obi wan](https://youtu.be/rEq1Z0bjdwc?si=P7c4XsN1BQj2ogdS)"
        links = extract_markdown_links(text)
        expected = [("A guide to vigilance", "https://youtu.be/dQw4w9WgXcQ?si=_4faL0F6NnUpr9cB"),
                     ("obi wan", "https://youtu.be/rEq1Z0bjdwc?si=P7c4XsN1BQj2ogdS"),]
        self.assertEqual(len(links), 2)
        self.assertListEqual(links, expected)