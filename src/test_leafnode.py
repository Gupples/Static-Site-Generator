import unittest

from leafnode import LeafNode

class TestLeafNode(unittest.TestCase):
    def test_leaf_to_html_p(self):
        node = LeafNode("p", "Hello, world!")
        expected = '<p>Hello, world!</p>'
        self.assertEqual(node.to_html(), expected)

    def test_leaf_to_html_p_with_props_one(self):
        props = {"href": "https://boot.dev"}
        node = LeafNode("p", "Hello, world!", props=props)
        expected = '<p href="https://boot.dev">Hello, world!</p>'
        self.assertEqual(node.to_html(), expected)

    def test_leaf_to_html_p_with_props_two(self):
        props = {"href": "https://boot.dev",
                 "target": "_blank"}
        node = LeafNode("p", "Hello, world!", props=props)
        expected = '<p href="https://boot.dev" target="_blank">Hello, world!</p>'
        self.assertEqual(node.to_html(), expected)
    
    def test_leaf_to_html_b(self):
        node = LeafNode("b", "This is bold text")
        expected = '<b>This is bold text</b>'
        self.assertEqual(node.to_html(), expected)
        