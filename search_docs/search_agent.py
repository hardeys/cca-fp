#!/usr/bin/env python3
"""
Search notes agent using Claude Agent SDK.
Searches local text files and answers questions based on their content.
Uses bash tool to search files instead of custom Python tool.
"""

import asyncio
import os
import sys
from pathlib import Path

from claude_agent_sdk import query, ClaudeAgentOptions, AssistantMessage


# Initialize the notes directory
NOTES_DIR = Path(os.getenv("NOTES_DIR", "./notes")).resolve()
if not NOTES_DIR.exists():
    NOTES_DIR.mkdir(parents=True, exist_ok=True)
    print(f"Created notes directory at {NOTES_DIR}")


async def main():
    """Main loop: read user queries and get agent responses."""
    print("Search Notes Agent")
    print("=" * 50)
    print(f"Notes directory: {NOTES_DIR}")
    print("Type 'exit' or 'quit' to exit, Ctrl-C to interrupt")
    print("=" * 50)
    print()

    # Initialize agent options
    # The agent can use bash to search files in the notes directory
    system_prompt = f"""You are a helpful assistant that searches and answers questions based on local notes.

You have access to bash to search files in: {NOTES_DIR}

When searching for information:
1. Use grep -r -i to search through all .txt files in the notes directory
2. Always cite where you found information (filename and line number)
3. If the search returns no results, clearly state that the information was not found in the notes
4. Do not make up information; only use what is in the search results

Example search: grep -r -i "python" {NOTES_DIR}/*.txt
"""

    options = ClaudeAgentOptions(system_prompt=system_prompt)

    try:
        while True:
            # Read user input
            try:
                user_input = input("You: ").strip()
            except EOFError:
                print("\n(End of input)")
                break
            except KeyboardInterrupt:
                print("\n(Interrupted)")
                break

            if not user_input:
                continue

            # Check for exit commands
            if user_input.lower() in ("exit", "quit"):
                print("Goodbye!")
                break

            # Query the agent
            print("\nAgent: ", end="", flush=True)
            try:
                # Collect the full response
                response_text = []
                async for event in query(
                    prompt=user_input,
                    options=options
                ):
                    # Look for AssistantMessage with content
                    if isinstance(event, AssistantMessage):
                        for block in event.content:
                            if hasattr(block, "text"):
                                response_text.append(block.text)

                if response_text:
                    full_text = "".join(response_text)
                    print(full_text)
                else:
                    print("(No text response)")

            except Exception as e:
                print(f"Error: {e}")
                import traceback
                traceback.print_exc()

            print()

    except Exception as e:
        print(f"\nFatal error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    asyncio.run(main())
