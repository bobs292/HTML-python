import os
from generatepage import generate_page

def generate_pages_recursive(dir_path_content, template_path, dest_dir_path, basepath="/"):
    """
    Generate HTML pages for all markdown files in a directory tree
    """
    # Walk through all files in the content directory
    for root, dirs, files in os.walk(dir_path_content):
        for file in files:
            if file.endswith('.md'):
                # Get the full path to the markdown file
                md_file_path = os.path.join(root, file)
                
                # Calculate the relative path from content_dir to this file
                rel_path = os.path.relpath(md_file_path, dir_path_content)
                
                # Replace .md extension with .html and create destination path
                html_rel_path = rel_path.replace('.md', '.html')
                dest_file_path = os.path.join(dest_dir_path, html_rel_path)
                
                print(f"Generating: {md_file_path} -> {dest_file_path}")
                
                # Generate the page
                generate_page(md_file_path, template_path, dest_file_path, basepath)