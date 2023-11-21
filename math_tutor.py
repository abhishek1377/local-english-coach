import openai
from gtts import gTTS
import os
import playsound
import speech_recognition as sr
from pathlib import Path


# Initialize OpenAI client
client = openai.OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# Step 1: Create an Assistant
assistant = client.beta.assistants.create(
    name="Math Tutor",
    instructions="You are a personal math tutor. Write and run code to answer math questions.",
    tools=[{"type": "code_interpreter"}],
    model="gpt-4-1106-preview"
)
# print("assitant", assistant)

# Step 2: Start a conversation thread
thread = client.beta.threads.create()
# print("thread:", thread, '\n')

# Step 3: Add user's message to the thread

message = client.beta.threads.messages.create(
    thread_id=thread.id,
    role="user",
    content="I need to solve the equation `3x + 11 = 14`. Can you help me?"
)
# print("message:", message, '\n')

# Step 4: Run the Assistant
run = client.beta.threads.runs.create(
  thread_id=thread.id,
  assistant_id=assistant.id,
)
# print("first run:", run, '\n')

# Check the status and retrieve response
run = client.beta.threads.runs.retrieve(
  thread_id=thread.id,
  run_id=run.id
)
# print("2nd run:", run, '\n')

# display the assistant reponse
messages = client.beta.threads.messages.list(
  thread_id=thread.id
)
# print("messages:", messages, '\n')

for message in reversed(messages.data):
    # print("messages", messages)
    print(message.role + ": " + message.content[0].text.value)

