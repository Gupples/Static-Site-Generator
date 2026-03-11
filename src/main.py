import os
import shutil
import sys
from textnode import TextNode, TextType
from generatecontent import generate_pages_recursive

def replace_files(source, destination):
    # Get the contents of the directory
    contents = os.listdir(source)

    # Create the destination directory if it doesn't exist
    if not os.path.exists(destination):
        os.mkdir(destination)

    # Copy items
    for item in contents:
        from_filepath = os.path.join(source, item)
        print(f"Copying item '{from_filepath}'.")
        to_filepath = os.path.join(destination, item)
        if os.path.isfile(from_filepath):
            shutil.copy(from_filepath, to_filepath)
        else:
            replace_files(from_filepath, to_filepath)

    # Make root path configurable
    basepath = sys.argv[1] if len(sys.argv) > 1 else '/'
        
    # Generate the page
    generate_pages_recursive("content", "template.html", "docs", basepath)

def main():
    # Refresh public contents
    if os.path.exists("docs"):
        shutil.rmtree("docs")
    replace_files("static", "docs")


if __name__ == "__main__":
    main() 
