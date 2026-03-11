import os
from block_markdown import markdown_to_html_node
from pathlib import Path


def extract_title(markdown):
    lines = markdown.split("\n")
    for line in lines:
        if line.startswith("# "):
            return line[2:].strip()
    raise Exception("No title found")
    
def generate_page(from_path, template_path, dest_path, basepath):
    print(f"Generating page from {from_path} to {dest_path} using {template_path}")
    with open(from_path, "r") as f:
        markdown = f.read()
    with open(template_path, "r") as t:
        template = t.read()
    html_node = markdown_to_html_node(markdown)
    html_string = html_node.to_html()
    title = extract_title(markdown)
    page = template.replace("{{ Title }}", title)
    page = page.replace("{{ Content }}", html_string)
    page = page.replace('href="/', f'href="{basepath}')
    page = page.replace('src="/', f'src="{basepath}')
    directory = os.path.dirname(dest_path)
    os.makedirs(directory, exist_ok=True)
    with open(dest_path, "w") as d:
        d.write(page)

def generate_pages_recursive(dir_path_content, template_path, dest_dir_path, basepath):
    content = os.listdir(dir_path_content)
    for item in content:
        new_dir_path = os.path.join(dir_path_content, item)
        new_dest_path = os.path.join(dest_dir_path, item)
        if not os.path.isfile(new_dir_path):
            generate_pages_recursive(new_dir_path, template_path, new_dest_path, basepath)
        else:
            path = Path(new_dest_path)
            new_dest_path = path.with_suffix(".html")
            generate_page(new_dir_path, template_path, new_dest_path, basepath)
    