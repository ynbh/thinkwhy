
import os
import datetime


# Using the LLM response, it is now time to put the responses into folders. 
def manage(note_dir,  classified_chunks):
    for chunk in classified_chunks:
        path = os.path.join(note_dir, chunk["path"])
        try:
            os.makedirs(os.path.dirname(path), exist_ok=True)
            with open(path, "a") as f:
                if f.tell() > 0:
                    f.write("\n\n---\n\n")
                f.write(chunk["text"])
        except Exception as e:
            print(f"Error writing to {path}: {e}")
            return False

    return True

# clear the inbox and archive it
def apply_changes(note_dir, classified_chunks, inbox_file="inbox.txt", archive_dir="archive"):
    print("Auto-tagging now...")
    manage(note_dir, classified_chunks)
    print("Auto-tagging completed successfully.")

    print("Archiving inbox...")
    os.makedirs(archive_dir, exist_ok=True)
    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    archive_path = os.path.join(archive_dir, f"inbox_{timestamp}.txt")
    
    if os.path.exists(inbox_file):
        os.rename(inbox_file, archive_path)
        print("Inbox archived successfully.")
    else:
        print(f"Warning: {inbox_file} not found, skipping archive.")

    # make a new inbox.txt file
    with open(inbox_file, "w") as f:
        f.write("")

    print("New inbox created successfully.")
