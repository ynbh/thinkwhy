# think why 

an intelligent note organization system powered by llms that automatically categorizes and files your notes.

## what it does

this tool provides a command-line interface to manage your notes, with features for adding, processing, refactoring, and browsing. the core feature is the ability to automatically categorize and file notes from an inbox file into a structured directory.

## setup

1. clone the repo
2. install dependencies:
   ```bash
   uv sync
   ```
3. create a `.env` file with your api key:
   ```
   AI_API_KEY=your_gemini_api_key_here
   ```

## usage

you can run the tool using the `manage` command:
```bash
uv run manage <command>
```

### commands

- `a`, `add <note>`: add a new note to `inbox.md`.
- `p`, `process`: process the notes in `inbox.md`, categorizing and filing them into the `notes/` directory.
- `r`, `refactor`: refactor the entire note structure in `notes/`.
- `b`, `browse`: launch an interactive tui to browse notes.
    - split-screen view with a directory tree and a markdown viewer.
    - the markdown viewer is scrollable.
    - press `escape` to close the file view.

### example workflow

1. add a note to your inbox:
   ```bash
   uv run manage add "solved leetcode problem 42 using a monotonic stack"
   ```
2. process the inbox:
   ```bash
   uv run manage process
   ```
3. browse your organized notes:
   ```bash
   uv run manage browse
   ```

## structure

```
manage/
├── src/
│   └── manage/
│       ├── __init__.py
│       ├── main.py
│       └── modules/
│           ├── __init__.py
│           ├── browse.py
│           ├── llm.py
│           ├── manage.py
│           └── parse.py
├── tests/
├── .gitignore
├── .python-version
├── pyproject.toml
├── README.md
└── uv.lock
```
