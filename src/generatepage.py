from blocktypes import extract_title, markdown_to_html_node
import os

def generate_page(from_path, template_path, dest_path, basepath="/"):
    print(f"Generating page from {from_path} to {dest_path} using {template_path}")
    
    # Read the markdown file
    with open(from_path, 'r') as f:
        markdown = f.read()
    
    # Read the template file
    with open(template_path, 'r') as t:
        template = t.read()
    
    # Extract title and convert markdown to HTML
    title = extract_title(markdown)
    node = markdown_to_html_node(markdown)
    html = node.to_html()
    
    # Replace basepath in href and src attributes in both template and content
    template = template.replace('href="/', f'href="{basepath}')
    template = template.replace('src="/', f'src="{basepath}')
    html = html.replace('href="/', f'href="{basepath}')
    html = html.replace('src="/', f'src="{basepath}')
    
    # Replace placeholders in template
    template = template.replace('{{ Title }}', title)
    template = template.replace('{{ Content }}', html)
    
    # Create destination directory if it doesn't exist
    dest_dir = os.path.dirname(dest_path)
    if dest_dir and not os.path.exists(dest_dir):
        os.makedirs(dest_dir)
    
    # Write the generated HTML to the destination file
    with open(dest_path, 'w') as d:
        d.write(template)


