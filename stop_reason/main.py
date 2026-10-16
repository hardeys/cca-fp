import os
from pathlib import Path
from dotenv import load_dotenv
from anthropic import Anthropic

load_dotenv(Path(__file__).parent.parent / ".env")

#read environemnt variable
anth_key=(os.getenv("ANTHROPIC_API_KEY"))
print (anth_key)
# get Anthropic client
client=Anthropic(api_key=anth_key)

message = client.messages.create(
    model="claude-opus-5-5",
    max_tokens=1024,
    messages=[{"role":"user","content":"Hello, Claude"}
    ]

)

for reply in message.content:
    if reply.type=="text":
        print(message.id)
        print(message.stop_reason)
        print(message.usage)
        print(message.content)