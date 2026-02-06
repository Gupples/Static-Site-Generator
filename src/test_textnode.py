import unittest

from textnode import TextNode, TextType, text_node_to_html_node
from leafnode import LeafNode

class TestTextNode(unittest.TestCase):
    def test_eq(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.BOLD)
        self.assertEqual(node, node2)

    def test_eq_url_not_none(self):
        node = TextNode("This is a text node", TextType.BOLD, "https://boot.dev")
        node2 = TextNode("This is a text node", TextType.BOLD, "https://boot.dev")
        self.assertEqual(node, node2)

    def test_eq_url_not_equal_one_none(self):
        node = TextNode("This is a text node", TextType.BOLD,)
        node2 = TextNode("This is a text node", TextType.BOLD, "https://boot.dev")
        self.assertNotEqual(node, node2)

    def test_eq_url_not_equal(self):
        node = TextNode("This is a text node", TextType.BOLD, "https://boot.dev")
        node2 = TextNode("This is a text node", TextType.BOLD, "https://different.url")
        self.assertNotEqual(node, node2)

    def test_eq_texttype_different(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.IMAGE)
        self.assertNotEqual(node, node2)

    # Test text_node_to_html_node()
    def test_text(self):
        node = TextNode("This is a text node", TextType.TEXT)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, None)
        self.assertEqual(html_node.value, "This is a text node")
        self.assertEqual(type(html_node), LeafNode)
        self.assertEqual(html_node.props, None)
    
    def test_bold(self):
        node = TextNode("This is a bold node", TextType.BOLD)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "b")
        self.assertEqual(html_node.value, "This is a bold node")
        self.assertEqual(type(html_node), LeafNode)
        self.assertEqual(html_node.props, None)

    def test_italic(self):
        node = TextNode("This is a italic node", TextType.ITALIC)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "i")
        self.assertEqual(html_node.value, "This is a italic node")
        self.assertEqual(type(html_node), LeafNode)
        self.assertEqual(html_node.props, None)

    def test_code(self):
        node = TextNode("This is a code node", TextType.CODE)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "code")
        self.assertEqual(html_node.value, "This is a code node")
        self.assertEqual(type(html_node), LeafNode)
        self.assertEqual(html_node.props, None)

    def test_link(self):
        node = TextNode("This is a link node", TextType.LINK, url="https://boot.dev")
        props = {"href": "https://boot.dev"}
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "a")
        self.assertEqual(html_node.value, "This is a link node")
        self.assertEqual(len(html_node.props), 1)
        self.assertEqual(html_node.props, props)
        self.assertEqual(type(html_node), LeafNode)

    def test_image(self):
        node = TextNode("This is an image node", TextType.IMAGE, "https://boot.dev")
        props = {"src": "https://boot.dev", "alt": "This is an image node"}
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "img")
        self.assertEqual(html_node.value, "")
        self.assertEqual(len(html_node.props.items()), 2)
        self.assertEqual(html_node.props, props)
        self.assertEqual(type(html_node), LeafNode)

    def test_invalid_text_type(self):
        with self.assertRaises(Exception) as e:
            node = TextNode("This should raise an error", "spaghetti code")
            html_node = text_node_to_html_node(node)
            print(html_node)
        self.assertEqual(str(e.exception), "Not a valid text type")


if __name__ == "__main__":
    unittest.main()