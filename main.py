import logging
from script.llm import make_client, process_inbox

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Define constants
NOTES_DIR = "notes"
INBOX_FILE = "inbox.md"
ARCHIVE_DIR = "archive"

def main():
    client = make_client()
    if not client:
        logging.error("Failed to create API client. Check your AI_API_KEY environment variable.")
        return
    
    process_inbox(client, INBOX_FILE, NOTES_DIR, ARCHIVE_DIR)

if __name__ == "__main__":
    main()
