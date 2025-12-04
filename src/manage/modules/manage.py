
import os
import datetime
import logging

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
            logging.error(f"Error writing to {path}: {e}")
            return False

    return True

def apply_changes(note_dir, classified_chunks, inbox_file, archive_dir="archive"):
    logging.info("Auto-tagging now...")
    manage(note_dir, classified_chunks)
    logging.info("Auto-tagging completed successfully.")

    logging.info("Archiving inbox...")
    os.makedirs(archive_dir, exist_ok=True)
    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    archive_path = os.path.join(archive_dir, f"inbox_{timestamp}.txt")
    
    if os.path.exists(inbox_file):
        os.rename(inbox_file, archive_path)
        logging.info("Inbox archived successfully.")
    else:
        logging.warning(f"Warning: {inbox_file} not found, skipping archive.")

    with open(inbox_file, "w") as f:
        f.write("")

    logging.info("New inbox created successfully.")


def apply_refactor(note_dir, refactor_plan):
    
    for move in refactor_plan.moves:
        old_path = os.path.join(note_dir, move.old_path)
        new_path = os.path.join(note_dir, move.new_path)
        
        # create the directory for the new path if it doesn't exist
        os.makedirs(os.path.dirname(new_path), exist_ok=True)
        
        # move the file
        os.rename(old_path, new_path)

    return 