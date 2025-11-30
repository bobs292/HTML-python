from extractLinks import extract_markdown_images, extract_markdown_links
from textnode import TextNode, TextType
def split_nodes_image(old_nodes):
    new_nodes = []
    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            new_nodes.append(node)
            continue

        original_text = node.text
        images = extract_markdown_images(original_text)  # list of (alt, url)

        if len(images) == 0:
            new_nodes.append(node)
            continue

        for alt, url in images:
            markdown = f"![{alt}]({url})"
            before, after = original_text.split(markdown, 1)

            if before != "":
                new_nodes.append(TextNode(before, TextType.TEXT))

            new_nodes.append(TextNode(alt, TextType.IMAGE, url))

            original_text = after

        if original_text != "":
            new_nodes.append(TextNode(original_text, TextType.TEXT))

    return new_nodes

def split_nodes_link(old_nodes):
    new_nodes = []
    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            new_nodes.append(node)
            continue
        original_text = node.text
        links = extract_markdown_links(original_text)

        if len(links) == 0:
            new_nodes.append(node)
            continue
        
        for text, link in links:
            markdown = f"[{text}]({link})"
            before, after = original_text.split(markdown,1)

            if before != "":
                new_nodes.append(TextNode(before, TextType.TEXT))
            
            new_nodes.append(TextNode(text, TextType.LINK, link))

            original_text = after
        if original_text != "":
            new_nodes.append(TextNode(original_text, TextType.TEXT))
    return new_nodes