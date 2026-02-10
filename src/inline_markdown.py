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

def split_nodes_image(old_nodes):
    new_nodes = []
    for node in old_nodes:
        images = extract_markdown_images(node.text)
        if images == []:
            new_nodes.append(node)
            continue
        to_split = node.text
        for i, (image_alt, image_link) in enumerate(images, start=1):
            sections = to_split.split(f"![{image_alt}]({image_link})", 1)
            if sections[0] != "":
                new_nodes.append(TextNode(sections[0], TextType.TEXT))
            new_nodes.append(TextNode(image_alt, TextType.IMAGE, image_link))
            if i == len(images):
                if sections[1] != "":
                    new_nodes.append(TextNode(sections[1], TextType.TEXT))
            else:
                to_split = sections[1]
    return new_nodes
    

def split_nodes_link(old_nodes):
    new_nodes = []
    for node in old_nodes:
        links = extract_markdown_links(node.text)
        if links == []:
            new_nodes.append(node)
            continue
        to_split = node.text
        for i, (link_text, url) in enumerate(links, start=1):
            sections = to_split.split(f"[{link_text}]({url})", 1)
            if sections[0] != "":
                new_nodes.append(TextNode(sections[0], TextType.TEXT))
            new_nodes.append(TextNode(link_text, TextType.LINK, url))
            if i == len(links):
                if sections[1] != "":
                    new_nodes.append(TextNode(sections[1], TextType.TEXT))
            else:
                to_split = sections[1]
    return new_nodes
    
