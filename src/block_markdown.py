from enum import Enum
import re
from parentnode import ParentNode
from textnode import *
from inline_markdown import text_to_textnodes


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

def text_to_children(block):
    inline_text_nodes = text_to_textnodes(block)
    leaf_nodes = []
    for text_node in inline_text_nodes:
        leaf_nodes.append(text_node_to_html_node(text_node))
    return leaf_nodes


def markdown_to_html_node(markdown):
    blocks = markdown_to_blocks(markdown)
    html_children = []
    for block in blocks:
        block_type = block_to_block_type(block)
        match block_type:
            case BlockType.HEADING:
                cleaned = block.lstrip("#")
                hashes = len(block) - len(cleaned)
                cleaned = cleaned.strip()
                heading_nodes = text_to_children(cleaned)
                html_children.append(ParentNode(f"h{hashes}", heading_nodes))
            case BlockType.QUOTE:
                block = block.split('\n')
                cleaned = [line.lstrip('>') for line in block]
                cleaned = '\n'.join(cleaned)
                quote_nodes = text_to_children(cleaned)
                html_children.append(ParentNode("blockquote", quote_nodes))
            case BlockType.UNORDERED_LIST:
                li_nodes = []
                block = block.split('\n')
                for line in block:
                    line = line[2:]
                    line_children = text_to_children(line)
                    li_nodes.append(ParentNode("li", line_children))
                html_children.append(ParentNode("ul", li_nodes))
            case BlockType.ORDERED_LIST:
                li_nodes = []
                block = block.split('\n')
                for line in block:
                    line = line.split('. ', 1)[1]
                    line_children = text_to_children(line)
                    li_nodes.append(ParentNode("li", line_children))
                html_children.append(ParentNode("ol", li_nodes))
            case BlockType.CODE:
                block = block[3:-3].lstrip('\n')
                text_node = TextNode(block, TextType.CODE)
                code_node = text_node_to_html_node(text_node)
                html_children.append(ParentNode("pre", [code_node]))
            case BlockType.PARAGRAPH:
                block = block.replace('\n', " ")
                p_nodes = text_to_children(block)
                html_children.append(ParentNode("p", p_nodes))
    return ParentNode("div", html_children)

            