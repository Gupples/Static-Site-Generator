import unittest

from htmlnode import HTMLNode

class TestHTMLNode(unittest.TestCase):
    def test_props_to_html_empty(self):
        node = HTMLNode()
        html = node.props_to_html()
        expected = ""
        self.assertEqual(html, expected)

    def test_props_to_html_one(self):
        props = {"href": "https://boot.dev"}
        node = HTMLNode(props=props)
        html = node.props_to_html()
        expected = ' href="https://boot.dev"'
        self.assertEqual(html, expected)

    def test_props_to_html_two(self):
        props = {"href": "https://boot.dev",
                 "target": "_blank"}
        node = HTMLNode(props=props)
        html = node.props_to_html()
        expected = ' href="https://boot.dev" target="_blank"'
        self.assertEqual(html, expected)
    
    def test_props_to_html_three(self):
        props = {"href": "https://boot.dev",
                 "target": "_blank",
                 "format": "css"}
        node = HTMLNode(props=props)
        html = node.props_to_html()
        expected = ' href="https://boot.dev" target="_blank" format="css"'
        self.assertEqual(html, expected)
