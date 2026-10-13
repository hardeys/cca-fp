# Search Notes Agent

An interactive agent that searches through local text files and answers questions based on their content. Built with the Claude Agent SDK.

## Features

- **Local text file search**: Searches all `.txt` files in a `notes/` directory
- **Interactive loop**: Ask questions until you type `exit` or `quit`
- **Tool use**: Agent uses bash/grep to search files efficiently
- **Cited results**: Answers include filename and line number references
- **Context awareness**: Maintains conversation history across multiple queries

## Setup

1. Create and activate a virtual environment:
```bash
python3 -m venv .venv
source .venv/bin/activate  # On macOS/Linux
# or
.venv\Scripts\activate  # On Windows
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Authenticate with Claude:
```bash
# If using Claude Code CLI
ant auth login
# or set your API key
export ANTHROPIC_API_KEY="sk-ant-..."
```

## Usage

Run the agent:
```bash
python search_agent.py
```

By default, it searches files in `./notes/` directory. To use a different directory:
```bash
NOTES_DIR=/path/to/notes python search_agent.py
```

### Example Session

```
Search Notes Agent
==================================================
Notes directory: ./notes
Type 'exit' or 'quit' to exit, Ctrl-C to interrupt
==================================================

You: What is Python?
Agent: According to your notes (sample.txt):
Python is a high-level programming language known for its simplicity and readability.
It's widely used in web development, data science, artificial intelligence, and automation.
...

You: exit
Goodbye!
```

## Adding Notes

Place any `.txt` files in the `notes/` directory. The agent will search across all of them.

Example `notes/my_notes.txt`:
```
Claude AI is developed by Anthropic.
Anthropic was founded in 2021.
Claude can help with coding, analysis, and creative writing.
```

Then ask questions:
```
You: Who founded Anthropic?
```

## Requirements

- Python 3.8+
- Claude API key (via `ANTHROPIC_API_KEY` or Claude Code CLI authentication)
- Dependencies in `requirements.txt`:
  - `claude-agent-sdk` - The Claude Agent SDK for building agents
  - `anthropic` - Anthropic Python SDK

## How It Works

1. User enters a query in the interactive loop
2. The agent receives the query with access to bash tools
3. The agent uses `grep` to search the notes directory for relevant content
4. Results are returned to the user with file references
5. Conversation continues until user exits

## Limitations

- Only searches plain text (`.txt`) files
- Search is case-insensitive (via `grep -i`)
- Limited to files directly in the notes directory (not subdirectories)
- Maximum 20 search hits returned per query

## License

See the main project LICENSE file.
