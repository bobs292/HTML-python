from textnode import TextNode, TextType
def split_nodes_delimiter(old_nodes, delimiter,text_type):
    final_node = []
    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            final_node.append(node)
            continue
        split_text = node.text.split(delimiter)
        if len(split_text) % 2 == 0:
            raise Exception("invalid markdown, formatted section not closed")
        for i, text in enumerate(split_text):
            if text == "":
                continue
            if i % 2 == 0:
                final_node.append(TextNode(text, TextType.TEXT))
            else:
                final_node.append(TextNode(text, text_type))
    return final_node