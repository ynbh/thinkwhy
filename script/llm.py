import json
from google.genai import Client
import os
from dotenv import load_dotenv 
from .parse import make_chunks, read_inbox, get_file_tree
from .manage import apply_changes
import re
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

load_dotenv()


def make_client():
    return Client(api_key=os.getenv("AI_API_KEY"))

def process_inbox(client, inbox_file, notes_dir, archive_dir):
    inbox = read_inbox(inbox_file)
    if not inbox.strip():
        logging.info("Inbox is empty. Nothing to process.")
        return

    chunks = make_chunks(inbox, r"\n---\s*\n")
    file_tree = get_file_tree(notes_dir)

    response = client.models.generate_content(
                    model="gemini-2.5-flash",
                    contents=[
                        (
                            """
                            You are an intelligent note organization assistant. Your task is to categorize and organize text chunks, which are provided in Markdown format.

                            ## Context
                            You will receive:
                            1. A file tree showing the current structure of the notes directory.
                            2. One or more text chunks that need to be organized. Each chunk is a Markdown entry, potentially spanning multiple lines.

                            ## Your Task
                            For each chunk:
                            1. **Analyze the content** to determine its topic and subtopic.
                            2. **Check the existing file tree** to see if a relevant category already exists.
                            3. **Decide on the appropriate file path**:
                               - If a matching category exists, use it.
                               - If a new category is needed, create a logical path for it.
                               - Create subcategories when appropriate (e.g., `learning/cs/algorithms/`).
                               - The file path MUST end with `.md` (e.g., "leetcode/dp/problem_notes.md").
                            4. **Enrich the text content**:
                               - Add a clear title (H1 heading) at the top if not present.
                               - Write a brief, concise summary of the note under a `## Summary` heading.
                               - Add relevant tags (e.g., `#tag1 #tag2`) at the end of the note.
                               - Ensure the output is clean and well-formatted Markdown.

                            ## Examples
                            - LeetCode problem about dynamic programming → `leetcode/dp/problem_notes.md`
                            - Interview preparation notes → `cs/interview/prep_notes.md`
                            - Daily journal entry → `daily_log/daily_entries.md`
                            - Project idea → `projects/project_name.md`

                            ## Output Format
                            Return a JSON array where each object has:
                            - `id`: the original chunk ID (integer)
                            - `text`: the enriched Markdown content (string), including title, summary, and tags.
                            - `path`: the file path relative to the notes directory (string). The path MUST end with `.md`.

                            Be thoughtful about file organization. Group related content together, but create new files when topics are distinct.
                            """
                        ).strip(),
                        (
                            f"""
                            File Tree:
                            {json.dumps(file_tree, indent=2)}
                            """
                        ).strip(),
                        json.dumps(chunks, indent=2),
                    ],
                )

    try:
        logging.info(response.text)
        match = re.search(r"```json\s*(.*?)\s*```", response.text, re.DOTALL)
        if match:
            text = match.group(1)
        else:
            text = response.text

        response_data = json.loads(text)
        if isinstance(response_data, dict):
            response_data = [response_data]

        input_ids = {c["id"] for c in chunks}
        output_ids = {r.get("id") for r in response_data}

        missing_ids = input_ids - output_ids
        if missing_ids:
            logging.warning(f"The following chunk IDs were not returned: {missing_ids}")
        else:
            logging.info(f"All {len(input_ids)} chunks were processed and returned.")
            apply_changes(notes_dir, response_data, inbox_file=inbox_file, archive_dir=archive_dir)

    except json.JSONDecodeError:
        logging.error("Failed to parse JSON response:")
        logging.error(response.text)
    except Exception as e:
        logging.error(f"An error occurred during verification: {e}")
