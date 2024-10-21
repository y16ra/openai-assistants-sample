import os
import json
import time
from openai import OpenAI
from dotenv import load_dotenv

# Load the environment variables
load_dotenv()

# Initialize the client
client = OpenAI()

VECTOR_STORE_ID = os.getenv("VECTOR_STORE_ID")

# Create a new assistant
assistant = client.beta.assistants.create(
    name="AI File Search Assistant",
    instructions="あなたはAIアシスタントです。指示がなければ日本語で回答します。",
    model="gpt-4o",
    tools=[{"type": "file_search"}],
    tool_resources={"file_search": {"vector_store_ids": [VECTOR_STORE_ID]}},
)
assistant_id =assistant.id
print(assistant_id)

# Create a new thread
thread = client.beta.threads.create()
print(thread.id)
thread_id = thread.id

# Send a message to the thread
prompt = "xxxx戦略について教えてください。"
thread_message = client.beta.threads.messages.create(
    thread_id,
    role="user",
    content=prompt,
)
print(thread_message)

# Run the assistant
run = client.beta.threads.runs.create(
    thread_id=thread_id,
    assistant_id=assistant_id,
)
run_id = run.id
print(run_id)

# Wait for the run to complete
while True:
    run = client.beta.threads.runs.retrieve(
        thread_id=thread_id,
        run_id=run_id
    )
    if run.status == "completed":
        break
    else:
        print(f"Waiting for completion... Current status: {run.status}")
    time.sleep(1)

# Get the messages from the thread
thread_messages = client.beta.threads.messages.list(thread_id)
for msg in thread_messages:
    if msg.content[0].type == "text":
        print(msg.role + "：" + msg.content[0].text.value)
