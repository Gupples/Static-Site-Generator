def markdown_to_blocks(markdown):
    raw_blocks = markdown.split("\n\n")
    new_blocks = []
    for block in raw_blocks:
        block = block.strip()
        block = block.strip("\n")
        if block != "":
            new_blocks.append(block)
    return new_blocks