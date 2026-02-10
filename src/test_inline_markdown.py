import unittest
from inline_markdown import *
from textnode import TextType, TextNode

class TestDelimiterSplitter(unittest.TestCase):
    def test_split_nodes_delimiter_pure_text(self):
        node = TextNode("This is a text node", TextType.TEXT)
        expected = [TextNode("This is a text node", TextType.TEXT)]
        new_nodes = split_nodes_delimiter([node], "`", TextType.CODE)
        self.assertEqual(len(new_nodes), 1)
        self.assertEqual(new_nodes, expected)
    
    def test_split_nodes_delimiter_pure_code(self):
        node = TextNode("This is a code block", TextType.CODE)
        expected = [TextNode("This is a code block", TextType.CODE)]
        new_nodes = split_nodes_delimiter([node], "`", TextType.CODE)
        self.assertEqual(len(new_nodes), 1)
        self.assertEqual(new_nodes, expected)

    def test_split_nodes_delimiter_code_block(self):
        node = TextNode("This is text with a `code block` word", TextType.TEXT)
        expected = [
            TextNode("This is text with a ", TextType.TEXT),
            TextNode("code block", TextType.CODE),
            TextNode(" word", TextType.TEXT),
            ]
        new_nodes = split_nodes_delimiter([node], "`", TextType.CODE)
        self.assertEqual(len(new_nodes), 3)
        self.assertEqual(new_nodes, expected)

    def test_split_nodes_delimiter_bold_block(self):
        node = TextNode("This is text with a **bold block** word", TextType.TEXT)
        expected = [
            TextNode("This is text with a ", TextType.TEXT),
            TextNode("bold block", TextType.BOLD),
            TextNode(" word", TextType.TEXT),
            ]
        new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
        self.assertEqual(len(new_nodes), 3)
        self.assertEqual(new_nodes, expected)

    def test_split_nodes_delimiter_italic_block(self):
        node = TextNode("This is text with a _italic block_ word", TextType.TEXT)
        expected = [
            TextNode("This is text with a ", TextType.TEXT),
            TextNode("italic block", TextType.ITALIC),
            TextNode(" word", TextType.TEXT),
            ]
        new_nodes = split_nodes_delimiter([node], "_", TextType.ITALIC)
        self.assertEqual(len(new_nodes), 3)
        self.assertEqual(new_nodes, expected)

    # ERRORS
    def test_split_nodes_delimiter_uneven_code(self):
        with self.assertRaises(Exception) as e:
            node = TextNode("This is an invalid `code block", TextType.TEXT)
            new_nodes = split_nodes_delimiter([node], "`", TextType.CODE)
            print(new_nodes)
        self.assertEqual(str(e.exception), "Invalid Markdown; no closing delimiter")

class TestImageSplitter(unittest.TestCase):
    def test_split_nodes_images_none(self):
        node = TextNode("This is text with nothing.", TextType.TEXT)
        expected = [TextNode("This is text with nothing.", TextType.TEXT),]
        new_nodes = split_nodes_image([node])
        self.assertEqual(len(new_nodes), 1)
        self.assertListEqual(new_nodes, expected)

    def test_split_nodes_images_one_end(self):
        node = TextNode("This is text with an image at the end. ![rick roll](https://i.imgur.com/e9twWaR.mp4)", TextType.TEXT)
        expected = [TextNode("This is text with an image at the end. ", TextType.TEXT),
                    TextNode("rick roll", TextType.IMAGE, "https://i.imgur.com/e9twWaR.mp4"),]
        new_nodes = split_nodes_image([node])
        self.assertEqual(len(new_nodes), 2)
        self.assertListEqual(new_nodes, expected)

    def test_split_nodes_images_one_middle(self):
        node = TextNode("This is text with a ![rick roll](https://i.imgur.com/e9twWaR.mp4) in the middle.", TextType.TEXT)
        expected = [TextNode("This is text with a ", TextType.TEXT),
                    TextNode("rick roll", TextType.IMAGE, "https://i.imgur.com/e9twWaR.mp4"),
                    TextNode(" in the middle.", TextType.TEXT),]
        new_nodes = split_nodes_image([node])
        self.assertEqual(len(new_nodes), 3)
        self.assertListEqual(new_nodes, expected)

    def test_split_nodes_images_two_start_end(self):
        node = TextNode("![rick roll](https://i.imgur.com/e9twWaR.mp4) Bookend images. ![obi wan](https://i.imgur.com/fJRm4Vk.jpeg)", TextType.TEXT)
        expected = [TextNode("rick roll", TextType.IMAGE, "https://i.imgur.com/e9twWaR.mp4"),
                    TextNode(" Bookend images. ", TextType.TEXT),
                    
                    TextNode("obi wan", TextType.IMAGE, "https://i.imgur.com/fJRm4Vk.jpeg")]
        new_nodes = split_nodes_image([node])
        self.assertEqual(len(new_nodes), 3)
        self.assertListEqual(new_nodes, expected)

    def test_split_nodes_images_two_middle_end(self):
        node = TextNode("An image here, ![rick roll](https://i.imgur.com/e9twWaR.mp4) and an image here![obi wan](https://i.imgur.com/fJRm4Vk.jpeg)", TextType.TEXT)
        expected = [TextNode("An image here, ", TextType.TEXT),
                    TextNode("rick roll", TextType.IMAGE, "https://i.imgur.com/e9twWaR.mp4"),
                    TextNode(" and an image here", TextType.TEXT),
                    
                    TextNode("obi wan", TextType.IMAGE, "https://i.imgur.com/fJRm4Vk.jpeg")]
        new_nodes = split_nodes_image([node])
        self.assertEqual(len(new_nodes), 4)
        self.assertListEqual(new_nodes, expected)

    def test_split_nodes_images_two_start_middle(self):
        node = TextNode("![rick roll](https://i.imgur.com/e9twWaR.mp4)An image here, and an image ![obi wan](https://i.imgur.com/fJRm4Vk.jpeg) there!", TextType.TEXT)
        expected = [TextNode("rick roll", TextType.IMAGE, "https://i.imgur.com/e9twWaR.mp4"),
                    TextNode("An image here, and an image ", TextType.TEXT),
                    
                    TextNode("obi wan", TextType.IMAGE, "https://i.imgur.com/fJRm4Vk.jpeg"),
                    TextNode(" there!", TextType.TEXT),]
        new_nodes = split_nodes_image([node])
        self.assertEqual(len(new_nodes), 4)
        self.assertListEqual(new_nodes, expected)

    def test_split_nodes_images_two_middle_middle_gap(self):
        node = TextNode("An image ![rick roll](https://i.imgur.com/e9twWaR.mp4) there, and an image ![obi wan](https://i.imgur.com/fJRm4Vk.jpeg) there!", TextType.TEXT)
        expected = [TextNode("An image ", TextType.TEXT),
                    TextNode("rick roll", TextType.IMAGE, "https://i.imgur.com/e9twWaR.mp4"),
                    TextNode(" there, and an image ", TextType.TEXT),
                    
                    TextNode("obi wan", TextType.IMAGE, "https://i.imgur.com/fJRm4Vk.jpeg"),
                    TextNode(" there!", TextType.TEXT),]
        new_nodes = split_nodes_image([node])
        self.assertEqual(len(new_nodes), 5)
        self.assertListEqual(new_nodes, expected)

    def test_split_nodes_images_two_middle_middle_adjacent(self):
        node = TextNode("An image here ![rick roll](https://i.imgur.com/e9twWaR.mp4)![obi wan](https://i.imgur.com/fJRm4Vk.jpeg) and there!", TextType.TEXT)
        expected = [TextNode("An image here ", TextType.TEXT),
                    TextNode("rick roll", TextType.IMAGE, "https://i.imgur.com/e9twWaR.mp4"),
                    TextNode("obi wan", TextType.IMAGE, "https://i.imgur.com/fJRm4Vk.jpeg"),
                    TextNode(" and there!", TextType.TEXT),]
        new_nodes = split_nodes_image([node])
        self.assertEqual(len(new_nodes), 4)
        self.assertListEqual(new_nodes, expected)

class TestLinkSplitter(unittest.TestCase):
    def test_split_nodes_link_none(self):
        node = TextNode("This is text with nothing.", TextType.TEXT)
        expected = [TextNode("This is text with nothing.", TextType.TEXT),]
        new_nodes = split_nodes_link([node])
        self.assertEqual(len(new_nodes), 1)
        self.assertListEqual(new_nodes, expected)

    def test_split_nodes_links_one_start(self):
        node = TextNode("[This](https://boot.dev) is a link at the beginning.", TextType.TEXT)
        expected = [TextNode("This", TextType.LINK, "https://boot.dev"),
                    TextNode(" is a link at the beginning.", TextType.TEXT),]
        new_nodes = split_nodes_link([node])
        self.assertEqual(len(new_nodes), 2)
        self.assertListEqual(new_nodes, expected)

    def test_split_nodes_links_one_middle(self):
        node = TextNode("There is a [link](https://boot.dev) in the middle.", TextType.TEXT)
        expected = [TextNode("There is a ", TextType.TEXT),
                    TextNode("link", TextType.LINK, "https://boot.dev"),
                    TextNode(" in the middle.", TextType.TEXT),]
        new_nodes = split_nodes_link([node])
        self.assertEqual(len(new_nodes), 3)
        self.assertListEqual(new_nodes, expected)

    def test_split_nodes_links_one_end(self):
        node = TextNode("This is text with a link at the [end.](https://boot.dev)", TextType.TEXT)
        expected = [TextNode("This is text with a link at the ", TextType.TEXT),
                    TextNode("end.", TextType.LINK, "https://boot.dev"),]
        new_nodes = split_nodes_link([node])
        self.assertEqual(len(new_nodes), 2)
        self.assertListEqual(new_nodes, expected)

    def test_split_nodes_links_two_start_end(self):
        node = TextNode("[This](https://www.youtube.com/watch?v=rEq1Z0bjdwc) is text with a link at the [end.](https://www.youtube.com/watch?v=dQw4w9WgXcQ)", TextType.TEXT)
        expected = [TextNode("This", TextType.LINK, "https://www.youtube.com/watch?v=rEq1Z0bjdwc"),
                    TextNode(" is text with a link at the ", TextType.TEXT),
                    TextNode("end.", TextType.LINK, "https://www.youtube.com/watch?v=dQw4w9WgXcQ"),]
        new_nodes = split_nodes_link([node])
        self.assertEqual(len(new_nodes), 3)
        self.assertListEqual(new_nodes, expected)

    def test_split_nodes_links_two_start_middle(self):
        node = TextNode("[This](https://www.youtube.com/watch?v=rEq1Z0bjdwc) is text with a [link](https://www.youtube.com/watch?v=dQw4w9WgXcQ) in the middle.", TextType.TEXT)
        expected = [TextNode("This", TextType.LINK, "https://www.youtube.com/watch?v=rEq1Z0bjdwc"),
                    TextNode(" is text with a ", TextType.TEXT),
                    TextNode("link", TextType.LINK, "https://www.youtube.com/watch?v=dQw4w9WgXcQ"),
                    TextNode(" in the middle.", TextType.TEXT),]
        new_nodes = split_nodes_link([node])
        self.assertEqual(len(new_nodes), 4)
        self.assertListEqual(new_nodes, expected)

    def test_split_nodes_links_two_middle_end(self):
        node = TextNode("There are links [here](https://www.youtube.com/watch?v=rEq1Z0bjdwc) and [there.](https://www.youtube.com/watch?v=dQw4w9WgXcQ)", TextType.TEXT)
        expected = [TextNode("There are links ", TextType.TEXT),
                    TextNode("here", TextType.LINK, "https://www.youtube.com/watch?v=rEq1Z0bjdwc"),
                    TextNode(" and ", TextType.TEXT),
                    TextNode("there.", TextType.LINK, "https://www.youtube.com/watch?v=dQw4w9WgXcQ"),]
        new_nodes = split_nodes_link([node])
        self.assertEqual(len(new_nodes), 4)
        self.assertListEqual(new_nodes, expected)

    def test_split_nodes_links_two_middle_middle_gap(self):
        node = TextNode("There are links [here](https://www.youtube.com/watch?v=rEq1Z0bjdwc) and [there](https://www.youtube.com/watch?v=dQw4w9WgXcQ), both in the middle.", TextType.TEXT)
        expected = [TextNode("There are links ", TextType.TEXT),
                    TextNode("here", TextType.LINK, "https://www.youtube.com/watch?v=rEq1Z0bjdwc"),
                    TextNode(" and ", TextType.TEXT),
                    TextNode("there", TextType.LINK, "https://www.youtube.com/watch?v=dQw4w9WgXcQ"),
                    TextNode(", both in the middle.", TextType.TEXT),]
        new_nodes = split_nodes_link([node])
        self.assertEqual(len(new_nodes), 5)
        self.assertListEqual(new_nodes, expected)

    def test_split_nodes_links_two_middle_middle_adjacent(self):
        node = TextNode("There are links [here ](https://www.youtube.com/watch?v=rEq1Z0bjdwc)[and there](https://www.youtube.com/watch?v=dQw4w9WgXcQ), both in the middle.", TextType.TEXT)
        expected = [TextNode("There are links ", TextType.TEXT),
                    TextNode("here ", TextType.LINK, "https://www.youtube.com/watch?v=rEq1Z0bjdwc"),
                    TextNode("and there", TextType.LINK, "https://www.youtube.com/watch?v=dQw4w9WgXcQ"),
                    TextNode(", both in the middle.", TextType.TEXT),]
        new_nodes = split_nodes_link([node])
        self.assertEqual(len(new_nodes), 4)
        self.assertListEqual(new_nodes, expected)


class TestExtractors(unittest.TestCase):
    def test_extract_markdown_images_none(self):
        text = "This string has no image"
        expected = []
        images = extract_markdown_images(text)
        self.assertEqual(len(images), 0)
        self.assertListEqual(images, expected)

    def test_extract_markdown_images_one(self):
        text = "This string has one image; ![rick roll](https://i.imgur.com/e9twWaR.mp4)"
        expected = [("rick roll", "https://i.imgur.com/e9twWaR.mp4")]
        images = extract_markdown_images(text)
        self.assertEqual(len(images), 1)
        self.assertListEqual(images, expected)

    def test_extract_markdown_images_two(self):
        text = "This string has some images; ![rick roll](https://i.imgur.com/e9twWaR.mp4) and ![obi wan](https://i.imgur.com/fJRm4Vk.jpeg)"
        expected = [("rick roll", "https://i.imgur.com/e9twWaR.mp4"),
                     ("obi wan", "https://i.imgur.com/fJRm4Vk.jpeg"),]
        images = extract_markdown_images(text)
        self.assertEqual(len(images), 2)
        self.assertListEqual(images, expected)

    def test_extract_markdown_links_none(self):
        text = "This string has no links"
        expected = []
        links = extract_markdown_links(text)
        self.assertEqual(len(links), 0)
        self.assertListEqual(links, expected)

    def test_extract_markdown_links_one(self):
        text = "This string has a link; [rick roll](https://www.youtube.com/watch?v=dQw4w9WgXcQ)"
        expected = [("rick roll", "https://www.youtube.com/watch?v=dQw4w9WgXcQ"),]
        links = extract_markdown_links(text)
        self.assertEqual(len(links), 1)
        self.assertListEqual(links, expected)

    def test_extract_markdown_links_some(self):
        text = "This string has some links; [A guide to vigilance](https://www.youtube.com/watch?v=dQw4w9WgXcQ) and [obi wan](https://www.youtube.com/watch?v=rEq1Z0bjdwc)"
        expected = [("A guide to vigilance", "https://www.youtube.com/watch?v=dQw4w9WgXcQ"),
                     ("obi wan", "https://www.youtube.com/watch?v=rEq1Z0bjdwc"),]
        links = extract_markdown_links(text)
        self.assertEqual(len(links), 2)
        self.assertListEqual(links, expected)

class TestTextnodeCreator(unittest.TestCase):
    def test_text_to_textnodes_full_singles(self):
        text = "This is **text** with an _italic_ word and a `code block` and an ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) and a [link](https://boot.dev)"
        expected = [TextNode("This is ", TextType.TEXT),
            TextNode("text", TextType.BOLD),
            TextNode(" with an ", TextType.TEXT),
            TextNode("italic", TextType.ITALIC),
            TextNode(" word and a ", TextType.TEXT),
            TextNode("code block", TextType.CODE),
            TextNode(" and an ", TextType.TEXT),
            TextNode("obi wan image", TextType.IMAGE, "https://i.imgur.com/fJRm4Vk.jpeg"),
            TextNode(" and a ", TextType.TEXT),
            TextNode("link", TextType.LINK, "https://boot.dev"),]
        nodes = text_to_textnodes(text)
        self.assertEqual(len(nodes), 10)
        self.assertListEqual(nodes, expected)