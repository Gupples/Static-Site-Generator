import unittest
from block_markdown import *

class TestBlockMarkdown(unittest.TestCase):
    def test_markdown_to_blocks_empty(self):
        md = ""
        expected = []
        blocks = markdown_to_blocks(md)
        self.assertEqual(len(blocks), 0)
        self.assertListEqual(blocks, expected)
    
    def test_markdown_to_blocks_new_lines_only_even(self):
        md = """





"""
        expected = []
        blocks = markdown_to_blocks(md)
        self.assertEqual(len(blocks), 0)
        self.assertListEqual(blocks, expected)

    def test_markdown_to_blocks_new_lines_only_odd(self):
        md = """






"""
        expected = []
        blocks = markdown_to_blocks(md)
        self.assertEqual(len(blocks), 0)
        self.assertListEqual(blocks, expected)

    def test_markdown_to_blocks_one_line_content(self):
        md = "This is a single block."
        expected = ["This is a single block."]
        blocks = markdown_to_blocks(md)
        self.assertEqual(len(blocks), 1)
        self.assertListEqual(blocks, expected)

    def test_markdown_to_blocks_one_line_content_with_new_line_before(self):
        md = """

This is a single block.
"""
        expected = ["This is a single block."]
        blocks = markdown_to_blocks(md)
        self.assertEqual(len(blocks), 1)
        self.assertListEqual(blocks, expected)

    def test_markdown_to_blocks_one_line_content_with_new_line_after(self):
        md = """
This is a single block.

"""
        expected = ["This is a single block."]
        blocks = markdown_to_blocks(md)
        self.assertEqual(len(blocks), 1)
        self.assertListEqual(blocks, expected)

    def test_markdown_to_blocks_three(self):
        md = """
This is **bolded** paragraph

This is another paragraph with _italic_ text and `code` here
This is the same paragraph on a new line

- This is a list
- with items
"""
        expected = ["This is **bolded** paragraph",
                    "This is another paragraph with _italic_ text and `code` here\nThis is the same paragraph on a new line",
                    "- This is a list\n- with items",]
        blocks = markdown_to_blocks(md)
        self.assertEqual(len(blocks), 3)
        self.assertListEqual(blocks, expected)
