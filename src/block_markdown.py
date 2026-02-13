from enum import Enum
import re

def markdown_to_blocks(markdown):
    raw_blocks = markdown.split("\n\n")
    new_blocks = []
    for block in raw_blocks:
        block = block.strip()
        block = block.strip("\n")
        if block != "":
            new_blocks.append(block)
    return new_blocks

BlockType = Enum("BlockType", ["PARAGRAPH", "HEADING", "CODE", "QUOTE", "UNORDERED_LIST", "ORDERED_LIST"])

def block_to_block_type(block):
    if re.match(r"^#{1,6} ", block):
        return BlockType.HEADING
    if block.startswith("```") and block.endswith("```"):
        return BlockType.CODE
    lines = block.split('\n')
    if all(line.startswith('>') for line in lines):
        return BlockType.QUOTE
    if all(line.startswith('- ') for line in lines):
        return BlockType.UNORDERED_LIST
    is_ordered_list = True
    for i, line in enumerate(lines, start=1):
        if not line.startswith(f"{i}. "):
            is_ordered_list = False
            break
    if is_ordered_list:
        return BlockType.ORDERED_LIST
    return BlockType.PARAGRAPH