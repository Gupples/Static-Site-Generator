from textnode import TextNode, TextType

def main():
    dummy_node = TextNode("This is the initial text", TextType("bold"), "https://url.com")
    dummy_node.__repr__()


if __name__ == "__main__":
    main() 