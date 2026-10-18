from pathlib import Path
from typing import Any, Dict, List, Union
from dotenv import load_dotenv
from anthropic import Anthropic

load_dotenv(Path(__file__).parent.parent / ".env")

# Anthropic() reads ANTHROPIC_API_KEY from the environment
client = Anthropic()
MODEL = "claude-sonnet-5-5"


# Helper functions for conversation history management

def add_user_message(conv_messages: List[Dict[str, Any]], content: Union[str, List[Dict[str, Any]]]) -> None:
    conv_messages.append({"role": "user", "content": content})


def add_assistant_message(conv_messages: List[Dict[str, Any]], message) -> None:
    conv_messages.append({"role": "assistant", "content": message.content})


def add_tool_result(conv_messages: List[Dict[str, Any]], tool_use_id: str, result_content: str) -> None:
    tool_result = {"type": "tool_result", "tool_use_id": tool_use_id, "content": result_content}
    conv_messages.append({"role": "user", "content": [tool_result]})


def get_text(message) -> str:
    """Join all text blocks of a response."""
    return "".join(block.text for block in message.content if block.type == "text")


# Sub-agents: each one is a single Claude call with its own system prompt.
# The weather agent also has a simulated data source (static temperature).

def get_temperature(city: str) -> str:
    return f"22C and partly cloudy in {city}"


def weather_agent(city: str) -> str:
    """Specialist agent: reports the weather for a city."""
    message = client.messages.create(
        model=MODEL,
        max_tokens=256,
        system="You are a weather agent. Reply in one short sentence using only the data given.",
        messages=[{"role": "user", "content": f"Data: {get_temperature(city)}. Report the weather."}],
    )
    return get_text(message)


def clothing_agent(weather: str) -> str:
    """Specialist agent: suggests what to wear for a given weather report."""
    message = client.messages.create(
        model=MODEL,
        max_tokens=256,
        system="You are a clothing advisor. Reply in one short sentence.",
        messages=[{"role": "user", "content": f"Weather: {weather}. What should I wear?"}],
    )
    return get_text(message)


# Map tool name -> sub-agent function, so the coordinator can dispatch by name
AGENTS = {
    "ask_weather_agent": lambda args: weather_agent(args["city"]),
    "ask_clothing_agent": lambda args: clothing_agent(args["weather"]),
}

# The coordinator sees each sub-agent as a tool
tools = [
    {
        "name": "ask_weather_agent",
        "description": "Ask the weather agent for the current weather of a city",
        "input_schema": {
            "type": "object",
            "properties": {"city": {"type": "string", "description": "city name"}},
            "required": ["city"],
        },
    },
    {
        "name": "ask_clothing_agent",
        "description": "Ask the clothing agent what to wear, given a weather report",
        "input_schema": {
            "type": "object",
            "properties": {"weather": {"type": "string", "description": "weather report text"}},
            "required": ["weather"],
        },
    },
]


def coordinator(user_request: str) -> str:
    """Coordinator agent: delegates to sub-agents until Claude reaches end_turn."""
    conv_messages: List[Dict[str, Any]] = []
    add_user_message(conv_messages, user_request)

    while True:
        message = client.messages.create(
            model=MODEL,
            max_tokens=1024,
            system="You are a coordinator. Use the specialist agents to answer, then summarise.",
            tools=tools,
            messages=conv_messages,
        )
        print(f"[coordinator] stop_reason = {message.stop_reason}")

        if message.stop_reason != "tool_use":
            return get_text(message)

        # Keep the assistant turn (with its tool_use blocks) in the history
        add_assistant_message(conv_messages, message)

        for block in message.content:
            if block.type == "tool_use":
                print(f"[coordinator] -> {block.name}({block.input})")
                result = AGENTS[block.name](block.input)
                print(f"[{block.name}] <- {result}")
                add_tool_result(conv_messages, block.id, result)


if __name__ == "__main__":
    print(coordinator("What is the weather in Melbourne and what should I wear?"))
