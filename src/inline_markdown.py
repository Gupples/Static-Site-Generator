import re
from textnode import TextNode, TextType

def split_nodes_delimiter(old_nodes, delimiter, text_type):
    new_nodes = []
    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            new_nodes.append(node)
            continue
        slices = node.text.split(delimiter)
        if len(slices) > 1 and len(slices) % 2 == 0:
            raise Exception("Invalid Markdown; no closing delimiter")
        if len(slices) == 1:
            new_nodes.append(node)
            continue
        for i, content in enumerate(slices):
            if content == "":
                continue
            if i % 2 == 0:
                new_nodes.append(TextNode(content, TextType.TEXT))
            else:
                new_nodes.append(TextNode(content, text_type))
    return new_nodes

def extract_markdown_images(text):
    return re.findall(r"!\[([^\[\]]*)\]\(([^\(\)]*)\)", text)



def extract_markdown_links(text):
    return re.findall(r"(?<!!)\[([^\[\]]*)\]\(([^\(\)]*)\)", text)

