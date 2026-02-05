import unittest
from leafnode import LeafNode
from parentnode import ParentNode

class TestParentNode(unittest.TestCase):
    def test_to_html_with_children(self):
        child_node = LeafNode("span", "child")
        parent_node = ParentNode("div", [child_node])
        expected = "<div><span>child</span></div>"
        self.assertEqual(parent_node.to_html(), expected)

    def test_to_html_with_grandchildren(self):
        grandchild_node = LeafNode("b", "grandchild")
        child_node = ParentNode("span", [grandchild_node])
        parent_node = ParentNode("div", [child_node])
        expected = "<div><span><b>grandchild</b></span></div>"
        self.assertEqual(parent_node.to_html(), expected)
        
    def test_to_html_no_children(self):
        with self.assertRaises(ValueError) as ve:
            parent_node = ParentNode(tag="div", 
                                     children=None, 
                                     props=None)
            print(parent_node.to_html())
        self.assertEqual(str(ve.exception), "No children")
    