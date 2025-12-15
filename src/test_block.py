from block import BlockType, block_to_block_type
import unittest

class TestBlockType(unittest.TestCase):
    def test_paragraph(self):
        block = "This is a simple paragraph."
        self.assertEqual(block_to_block_type(block), BlockType.PARAGRAPH)

    def test_heading(self):
        block = "# This is a heading"
        self.assertEqual(block_to_block_type(block), BlockType.HEADING)

    def test_code(self):
        block = "```python\nprint('Hello, world!')\n```"
        self.assertEqual(block_to_block_type(block), BlockType.CODE)

    def test_quote(self):
        block = "> This is a quote."
        self.assertEqual(block_to_block_type(block), BlockType.QUOTE)

    def test_unordered_list(self):
        block = "- Item 1\n- Item 2\n- Item 3"
        self.assertEqual(block_to_block_type(block), BlockType.UNORDERED_LIST)

    def test_ordered_list(self):
        block = "1. First item\n2. Second item\n3. Third item"
        self.assertEqual(block_to_block_type(block), BlockType.ORDERED_LIST)

    def test_block_to_block_types(self):
        block = "# heading"
        self.assertEqual(block_to_block_type(block), BlockType.HEADING)
        block = "```\ncode\n```"
        self.assertEqual(block_to_block_type(block), BlockType.CODE)
        block = "> quote\n> more quote"
        self.assertEqual(block_to_block_type(block), BlockType.QUOTE)
        block = "- list\n- items"
        self.assertEqual(block_to_block_type(block), BlockType.UNORDERED_LIST)
        block = "1. list\n2. items"
        self.assertEqual(block_to_block_type(block), BlockType.ORDERED_LIST)
        block = "paragraph"
        self.assertEqual(block_to_block_type(block), BlockType.PARAGRAPH)
