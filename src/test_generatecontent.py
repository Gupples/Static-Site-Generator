import unittest
from generatecontent import extract_title

class TestGenerateContent(unittest.TestCase):
    def test_extract_title_no_title_one_line(self):
        with self.assertRaises(Exception) as e:
            markdown = """
This markdown has no title and only one line.
"""
            title = extract_title(markdown)
            print(title)
        self.assertEqual(str(e.exception), "No title found")
        
    def test_extract_title_no_title_many_lines(self):
        with self.assertRaises(Exception) as e:
            markdown = """
This markdown has no title and many lines.
This is another line.

However many lines there may be, no title will be found.
"""
            title = extract_title(markdown)
            print(title)
        self.assertEqual(str(e.exception), "No title found")
        
    def test_extract_title_one_line_is_title(self):
        markdown = """
# This is the content of the title.
"""
        expected = "This is the content of the title."
        title = extract_title(markdown)
        self.assertEqual(expected, title)
        
    def test_extract_title_one_line_is_title_with_whitespace(self):
        markdown = """
# This is the content of the title.        
"""
        expected = "This is the content of the title."
        title = extract_title(markdown)
        self.assertEqual(expected, title)
        
    def test_extract_title_many_lines_top(self):
        markdown = """
# This is the content of the title.
This is more content found in the markdown.
"""
        expected = "This is the content of the title."
        title = extract_title(markdown)
        self.assertEqual(expected, title)
        
    def test_extract_title_many_lines_middle(self):
        markdown = """
##### This is not the title.
# This is the content of the title.
This is more content found in the markdown.
"""
        expected = "This is the content of the title."
        title = extract_title(markdown)
        self.assertEqual(expected, title)