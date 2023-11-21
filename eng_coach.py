import openai
from gtts import gTTS
import os
import playsound
import speech_recognition as sr
from pathlib import Path
import time

def recognize_speech_from_mic():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        audio = recognizer.listen(source, timeout=5)
        try:
            text = recognizer.recognize_google(audio)
            return text if text else None
        except sr.UnknownValueError:
            return None
        except sr.RequestError:
            return "Could not request results from Google Speech Recognition service"

def get_response_from_openai(text, client):
    response = client.chat.completions.create(
        model= "gpt-4",
        messages=[{"role": "user", "content": text}]
    )
    return response.choices[0].text.strip()

def text_to_speech(text, client):
    speech_file_path = Path(__file__).parent / "speech.mp3"
    print("speech_file_path:", speech_file_path)
    try:
        speech_response = client.audio.speech.create(
            model="tts-1",
            voice="nova",
            input=text
        )
        speech_response.stream_to_file(str(speech_file_path))
        playsound.playsound(str(speech_file_path))
    except Exception as e:
        print("An error occurred in text-to-speech:", e)

# Initialize OpenAI client
client = openai.OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# Step 1: Create an Assistant
# assistant = client.beta.assistants.create(
#     name="Math Tutor",
#     instructions="You are a personal math tutor. Write and run code to answer math questions.",
#     tools=[{"type": "code_interpreter"}],
#     model="gpt-4-1106-preview"
# )

# Step 2: Start a conversation thread
thread = client.beta.threads.create()
print("thread:", thread, '\n')
exit_keywords = ["exit", "end", "goodbye", "terminate"]

while True:
    # Speech recognition
    speech_text = recognize_speech_from_mic()
    
    # If no input is detected, prompt again
    if speech_text is None:
        print("No speech detected, please try again.")
        continue

    # Check user input for exit keywords
    if any(word in speech_text.lower() for word in exit_keywords):
        print("User indicated to stop the conversation.")
        break

    # Step 3: Add user's message to the thread
    message = client.beta.threads.messages.create(thread_id=thread.id, role="user", content=speech_text)
    # print("message:", message, '\n')

    # Step 4: Run the Assistant
    run = client.beta.threads.runs.create(thread_id=thread.id, assistant_id="asst_1YsovcLtOVS0teglsurZBnn0")
    
    # print("running the assistant:", run)

    # Check the status and retrieve response
    run = client.beta.threads.runs.retrieve(
            thread_id=thread.id,
            run_id=run.id
            )

    while True:
        run_status = client.beta.threads.runs.retrieve(
            thread_id=thread.id,
            run_id=run.id
        )
        # Check if the run is completed
        if run_status.status == 'completed':
            break
        # Wait for a short period before checking again
        # print("waiting for response")
        time.sleep(1)  # 2 seconds delay

    # print("response receival:", run.status, '\n')

    # display the assistant reponse
    messages = client.beta.threads.messages.list(
    thread_id=thread.id
    )

    # print("messages:", messages, '\n')

    for message in reversed(messages.data):
        # print("messages", messages)
        print(message.role + ": " + message.content[0].text.value)

    response_text = messages.data[0].content[0].text.value

    # Step 5: Convert response to speech and play it
    text_to_speech(response_text, client)
    
