import logging
import click
from script.llm import make_client, process_inbox, refactor
from script.parse import get_file_tree
from script.browse import NotesBrowser
import json

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

NOTES_DIR = "notes"
INBOX_FILE = "inbox.md"
ARCHIVE_DIR = "archive"

@click.group()
def cli():
    """a command-line tool to manage your notes."""
    pass

@cli.command(help="process the inbox and organize the notes.")
def process():
    """processes the inbox."""
    client = make_client()
    if not client:
        logging.error("Failed to create API client. Check your AI_API_KEY environment variable.")
        return
    
    process_inbox(client, INBOX_FILE, NOTES_DIR, ARCHIVE_DIR)
    logging.info("Inbox processing complete.")

@cli.command(help="add a new note to the inbox.")
@click.argument('note_text', required=True)
def add(note_text):
    """adds a note to the inbox."""
    with open(INBOX_FILE, "a") as f:
        if f.tell() > 0: # if the file is not empty, add a separator first for the new chunk 
            f.write("\n\n---\n\n")
        f.write(note_text)
    logging.info(f"Added note to {INBOX_FILE}.")

@cli.command(help="refactor the entire note structure")
def refactor_notes():
    """refactors the notes."""
    client = make_client()
    if not client:
        logging.error("Failed to create API client. Check your AI_API_KEY environment variable.")
        return
    logging.info("Refactoring...")
    refactor(client, NOTES_DIR)
    logging.info("Refactoring complete.")

@cli.command(name="browse", help="browse your notes interactively.")
@click.option("--notes-dir", default="notes", help="directory containing notes.")
def browse_command(notes_dir):
    """launches an interactive notes browser."""
    app = NotesBrowser(notes_dir)
    app.run()


if __name__ == "__main__":
    cli.add_command(process, "p")
    cli.add_command(refactor_notes, "r")
    cli.add_command(add, "a")
    cli.add_command(browse_command, "b")
    cli()
