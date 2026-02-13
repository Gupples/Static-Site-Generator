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


    def test_block_to_block_type_paragraph_one_line(self):
        md = """
This is a normal paragraph.
"""
        block_type = block_to_block_type(md.strip())
        self.assertEqual(block_type, BlockType.PARAGRAPH)

    def test_block_to_block_type_paragraph_multiple_lines_solid(self):
        md = """
This is a normal paragraph.
It has a number of lines.
They are all together.
"""
        block_type = block_to_block_type(md.strip())
        self.assertEqual(block_type, BlockType.PARAGRAPH)

    def test_block_to_block_type_paragraph_code_without_start(self):
        md = """
This is supposed to be a code block,
but it's missing the first three '`' characters.
```
"""
        block_type = block_to_block_type(md.strip())
        self.assertEqual(block_type, BlockType.PARAGRAPH)

    def test_block_to_block_type_paragraph_code_without_end(self):
        md = """
```
This is supposed to be a code block,
but it's missing the last three '`' characters.
"""
        block_type = block_to_block_type(md.strip())
        self.assertEqual(block_type, BlockType.PARAGRAPH)

    def test_block_to_block_type_paragraph_inconsistent_quotes(self):
        md = """
> This would normally be a quote block,
> but it is broken by
this single line.
"""
        block_type = block_to_block_type(md.strip())
        self.assertEqual(block_type, BlockType.PARAGRAPH)
        
    def test_block_to_block_type_paragraph_inconsistent_unordered_list(self):
        md = """
- This would normally be an unordered list
- but it is broken by
this single line.
"""
        block_type = block_to_block_type(md.strip())
        self.assertEqual(block_type, BlockType.PARAGRAPH)
        
    def test_block_to_block_type_paragraph_unordered_list_no_space(self):
        md = """
- This would normally be an unordered list
- but it is broken by
-this single line.
"""
        block_type = block_to_block_type(md.strip())
        self.assertEqual(block_type, BlockType.PARAGRAPH)
        
    def test_block_to_block_type_paragraph_inconsistent_ordered_list(self):
        md = """
1. This would normally be an unordered list
2. but it is broken by
this single line.
"""
        block_type = block_to_block_type(md.strip())
        self.assertEqual(block_type, BlockType.PARAGRAPH)
        
    def test_block_to_block_type_paragraph_constant_ordered_list(self):
        md = """
1. This would normally be an unordered list
1. but it is broken by
1. all the ones in the list.
"""
        block_type = block_to_block_type(md.strip())
        self.assertEqual(block_type, BlockType.PARAGRAPH)
        
    def test_block_to_block_type_paragraph_ordered_list_starts_by_0(self):
        md = """
0. This would normally be an unordered list
1. but it is broken by
2. starting with 0.
"""
        block_type = block_to_block_type(md.strip())
        self.assertEqual(block_type, BlockType.PARAGRAPH)
        
    def test_block_to_block_type_paragraph_too_many_hashes(self):
        md = """
####### There are 7 hashes in this line. The parameter is 6 and a space.
"""
        block_type = block_to_block_type(md.strip())
        self.assertEqual(block_type, BlockType.PARAGRAPH)
        
    def test_block_to_block_type_paragraph_heading_no_space(self):
        md = """
######There are 6 hashes in this line. The parameter is 6 and a space.
"""
        block_type = block_to_block_type(md.strip())
        self.assertEqual(block_type, BlockType.PARAGRAPH)
        
    def test_block_to_block_type_heading_one_line(self):
        md = """
###### This should be a single-lined header.
"""
        block_type = block_to_block_type(md.strip())
        self.assertEqual(block_type, BlockType.HEADING)
        
    def test_block_to_block_type_heading_many_lines(self):
        md = """
###### This should be a multi-lined header.
It should not matter that this line does not start with hashes.
"""
        block_type = block_to_block_type(md.strip())
        self.assertEqual(block_type, BlockType.HEADING)
        
    def test_block_to_block_type_code_no_content(self):
        md = """
``````
"""
        block_type = block_to_block_type(md.strip())
        self.assertEqual(block_type, BlockType.CODE)
        
    def test_block_to_block_type_code_one_line(self):
        md = """
```
This should still be code.
```
"""
        block_type = block_to_block_type(md.strip())
        self.assertEqual(block_type, BlockType.CODE)
        
    def test_block_to_block_type_code_multiple_lines(self):
        md = """
```
This should still be code.
It should not matter; this should still be code.
```
"""
        block_type = block_to_block_type(md.strip())
        self.assertEqual(block_type, BlockType.CODE)
        
    def test_block_to_block_type_quote_no_content(self):
        md = """
>
"""
        block_type = block_to_block_type(md.strip())
        self.assertEqual(block_type, BlockType.QUOTE)
        
    def test_block_to_block_type_quote_one_line(self):
        md = """
> This should be a quote
"""
        block_type = block_to_block_type(md.strip())
        self.assertEqual(block_type, BlockType.QUOTE)
        
    def test_block_to_block_type_quote_multiple_lines(self):
        md = """
> This should be a quote.
> This should still be a quote.
"""
        block_type = block_to_block_type(md.strip())
        self.assertEqual(block_type, BlockType.QUOTE)
        
    def test_block_to_block_type_unordered_list_no_content(self):
        md = "- "
        block_type = block_to_block_type(md)
        self.assertEqual(block_type, BlockType.UNORDERED_LIST)
        
    def test_block_to_block_type_unordered_list_one_item(self):
        md = """
- Unordered item #1
"""
        block_type = block_to_block_type(md.strip())
        self.assertEqual(block_type, BlockType.UNORDERED_LIST)
        
    def test_block_to_block_type_unordered_list_multiple_items(self):
        md = """
- Unordered item #1
- Unordered item #2
"""
        block_type = block_to_block_type(md.strip())
        self.assertEqual(block_type, BlockType.UNORDERED_LIST)
        
    def test_block_to_block_type_ordered_list_one_item(self):
        md = """
1. First item
"""
        block_type = block_to_block_type(md.strip())
        self.assertEqual(block_type, BlockType.ORDERED_LIST)
        
    def test_block_to_block_type_ordered_list_multiple_items(self):
        md = """
1. First item
2. Second item
3. Third item
"""
        block_type = block_to_block_type(md.strip())
        self.assertEqual(block_type, BlockType.ORDERED_LIST)
    
