import os
import shutil
from textnode import TextNode, TextType

def replace_files(source, destination):
    # Get the contents of the directory
    contents = os.listdir(source)

    # Create the source directory if it doesn't exist
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

def main():
    # Refresh public contents
    if os.path.exists("public"):
        shutil.rmtree("public")
    replace_files("static", "public")


if __name__ == "__main__":
    main() 