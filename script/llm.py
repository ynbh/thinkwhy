import json
from google.genai import Client
import os
from dotenv import load_dotenv 
from parse import make_chunks, read_inbox, get_file_tree
from manage import apply_changes
import re
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

load_dotenv()


def make_client():
    return Client(api_key=os.getenv("AI_API_KEY"))

client = make_client()

inbox = read_inbox("inbox.txt")
chunks = make_chunks(inbox, r"\n--\s*\n")
file_tree = get_file_tree("notes")

response = client.models.generate_content(
                model="gemini-2.5-flash",
                contents=[
                    (
                        """
                        You are a tool that can auto-tag chunks of text based on their content. When I say auto-tag, I mean that you will 
                        first be given information about the file structure of a directory called notes. This directory contains 
                        notes from different aspects of the user's life. The file structure could be anything. Your job is to take in
                        the new chunks of text added to notes, figure out what topic/subtopic they belong to, and tag them accordingly. 

                        For example:
                        - if the chunk of text is about LeetCode, and specficaly about a topic, you job is to:
                            - Check the file structure of the notes directory 
                            - If the topic already exists, tag the chunk of text with the topic. There is opportunity for further subtopic creation here if you feel the need. E.g. Stack under Leetcode, Monotonic Stack under Stack. 
                            - If the topic does not exist, create a new folder for the topic, and tag the chunk of text with the topic. 

                        Your response MUST be in JSON, and should contain:
                        - the newly formatted text of the chunk. It should be tagged "text", and have its contents in markdown. 
                        - where in the notes directory the chunk should be: e.g. leetcode/stack/monotonic_stack.md
                        - the original id of the chunk, tagged as "id"
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

        apply_changes("notes", response_data)

except json.JSONDecodeError:
    logging.error("Failed to parse JSON response:")
    logging.error(response.text)
except Exception as e:
    logging.error(f"An error occurred during verification: {e}")
