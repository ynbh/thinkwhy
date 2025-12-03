
import os
import re

"""
this module provides functions for parsing text and file structures.
"""

def read_inbox(file_path):
    with open(file_path , "r") as f:
        return f.read()

def make_chunks(text, delimiter):

    chunks = re.split(delimiter, text)
    cleaned = [c.strip() for c in chunks if c.strip()]

    return [{"id": idx, "text": chunk} for idx, chunk in enumerate(cleaned)]

# pass in the file tree to give the LLM context about the file structure.
def get_file_tree(notes_dir):
    
    files = os.listdir(notes_dir)
    tree = []

    # this could have nested folders 
    for f in files:
        if os.path.isdir(os.path.join(notes_dir, f)):
            tree.append({"name": f, "type": "folder", "files": []})
            files = get_file_tree(os.path.join(notes_dir, f))
            tree[-1]["files"] = files
        else:
            tree.append({"name": f, "type": "file"})

    return tree

if __name__ == "__main__":
    inbox = read_inbox() 
    print(get_file_tree("notes"))