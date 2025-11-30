import os
import shutil
import sys

from copystatic import copy_files_recursive
from generatepage import generate_page
from generatepages import generate_pages_recursive

dir_path_static = "./static"
dir_path_docs = "./docs"

def main():
    # Get basepath from command line arguments, default to "/"
    basepath = "/"
    if len(sys.argv) > 1:
        basepath = sys.argv[1]
    
    print(f"Using basepath: {basepath}")
    
    print("Deleting docs directory...")
    if os.path.exists(dir_path_docs):
        shutil.rmtree(dir_path_docs)

    print("Copying static files to docs directory...")
    copy_files_recursive(dir_path_static, dir_path_docs)
    
    print("Generating pages for all markdown files...")
    generate_pages_recursive("./content", "./template.html", "./docs", basepath)

main()
