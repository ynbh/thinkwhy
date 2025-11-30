
import os
"""
parses inbox.txt, archives it, and deletes the contents of inbox.txt. 
"""

def read_inbox(file_path = "inbox.txt"):
    with open(file_path , "r") as f:
        return f.read()


import re

def make_chunks(text, delimiter):

    chunks = re.split(delimiter, text)
    cleaned = [c.strip() for c in chunks if c.strip()]

    return [{"id": idx, "text": chunk} for idx, chunk in enumerate(cleaned)]

"""
We pass in the file tree to give the LLM context about the file structure.
"""
def get_file_tree(notes_dir):
    
    files = os.listdir(notes_dir)
    ans = []

    # this could have nested folders 
    for f in files:
        if os.path.isdir(os.path.join(notes_dir, f)):
            ans.append({"name": f, "type": "folder", "files": []})
            files = get_file_tree(os.path.join(notes_dir, f))
            ans[-1]["files"] = files
        else:
            ans.append({"name": f, "type": "file"})

    return ans

if __name__ == "__main__":
    inbox = read_inbox() 
    print(get_file_tree("notes"))