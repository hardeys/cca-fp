import os
from pathlib import Path
from typing import List, Dict, Any, Union
from dotenv import load_dotenv
from anthropic import Anthropic

load_dotenv(Path(__file__).parent.parent / ".env")

#read anthropic key from the env variable
anth_key=(os.getenv("ANTHROPIC_API_KEY"))

#create a enthropic client

client = Anthropic(api_key=anth_key)
MODEL = "claude-opus-5-5"
conv_messages = []

# Helper functions for conversation history management

def add_user_message(conv_messages: List[Dict[str, Any]], content: Union[str, List[Dict[str, Any]]]) -> None:
    """
    Append a user message to the conversation history.

    Args:
        conv_messages: The conversation history list to mutate
        content: String or list of content blocks for the user message
    """
    conv_messages.append({"role": "user", "content": content})


def add_assistant_message(conv_messages: List[Dict[str, Any]], message) -> None:
    """
    Append an assistant response to the conversation history.

    Args:
        conv_messages: The conversation history list to mutate
        message: Anthropic Message object from API response
    """
    conv_messages.append({"role": "assistant", "content": message.content})


def add_tool_result(conv_messages: List[Dict[str, Any]], tool_use_id: str, result_content: Union[str, Dict[str, Any]], is_error: bool = False) -> None:
    """
    Append a tool result message to the conversation history.

    Args:
        conv_messages: The conversation history list to mutate
        tool_use_id: The ID from the tool_use block
        result_content: String or JSON-serializable result from tool execution
        is_error: Whether this is an error result (default: False)
    """
    tool_result = {
        "type": "tool_result",
        "tool_use_id": tool_use_id,
        "content": str(result_content)
    }

    if is_error:
        tool_result["is_error"] = True

    conv_messages.append({"role": "user", "content": [tool_result]})


#print Response from Cluade
def printmessage(title, message):
    print("-"*60)
    print(title)
    print(f'Stop Reason is: {message.stop_reason}')
    print(f'Output Token used are {message.usage.output_tokens}')
    print(f'Input Token used are {message.usage.input_tokens}')
    for block in message.content:
        if (block.type == "text"):
            print(f'Content type is {block.type}')
            print(f'content: {block.text}')
        elif (block.type == "tool_use"):
            print (f'Tool Name: {block.name}')
            print (f'Tool id: {block.id}')
            print (f'Tool input: {block.input}')
    print()


# end_turn stop reason use case
add_user_message(conv_messages, "Hello Claude, today we will be checking some weather stats")
message = client.messages.create(
    model = MODEL,
    max_tokens = 1024,
    messages = conv_messages)

printmessage("1. stop_reason = end_turn: ", message)

add_assistant_message(conv_messages, message)

# defining tools

tools = [

    {
        "name": "get_weather",
        "description":"Get the current weather of the city",
        "input_schema": {
            "type":"object",
            "properties":{
                "city":{"type":"string", "description":"city name"}
            },
            "required":["city"]
        }       
    }
]

add_user_message(conv_messages, "What is the weather in Melbourne")

message = client.messages.create(
    model=MODEL,
    max_tokens=1024,
    tools=tools,
    messages=conv_messages)

printmessage("2. stop_reason = tool_use",message)
