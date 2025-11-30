# manage

an intelligent note organization system powered by llms that automatically categorizes and files your notes.

## what it does

drop quick notes into `inbox.txt`, separated by `--`, and the system will:
- analyze each note's content
- determine the appropriate category and file path
- format it in markdown
- append it to the right file in your `notes/` directory
- archive the processed inbox

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

1. add notes to `inbox.txt`, separating each with `--`:
   ```
   solved leetcode problem 42 using monotonic stack
   
   --
   
   had a great interview prep session today
   
   --
   
   new project idea: build a cli tool for managing todos
   ```

2. run the script:
   ```bash
   uv run script/llm.py
   ```

3. your notes are now organized in the `notes/` directory and the inbox is archived

## structure

```
manage/
├── inbox.txt          # drop your notes here
├── notes/             # organized notes (gitignored)
├── archive/           # processed inboxes (gitignored)
└── script/
    ├── llm.py         # main script
    ├── parse.py       # parsing utilities
    └── manage.py      # file management
```

## features

- **smart categorization**: uses gemini to understand context and organize notes
- **append mode**: preserves existing notes, doesn't overwrite
- **flexible delimiters**: handles `--` with or without extra spaces
- **automatic archiving**: keeps a history of all processed inboxes
- **error handling**: robust file operations with proper logging

## notes

- the `notes/` directory is gitignored by default
- archived inboxes are timestamped for easy reference
- the system appends to existing files, so related notes stay together
