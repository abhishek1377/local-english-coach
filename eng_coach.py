import openai
from gtts import gTTS
import os
import playsound
import speech_recognition as sr
from pathlib import Path

def recognize_speech_from_mic():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        audio = recognizer.listen(source)
        try:
            text = recognizer.recognize_google(audio)
            return text
        except sr.UnknownValueError:
            return "Google Speech Recognition could not understand audio"
        except sr.RequestError:
            return "Could not request results from Google Speech Recognition service"

def get_response_from_openai(text,client):
    
    response = client.chat.completions.create(
        messages=[{"role": "user", "content": text}],
        model="gpt-4"
    )
    return response.choices[0].message.content

def text_to_speech(text, client):
    speech_file_path = Path(__file__).parent / "speech.mp3"
    print("speech_file_path:", speech_file_path)
    try:
        speech_response = client.audio.speech.create(
            model="tts-1",
            voice="alloy",
            input=text
        )
        speech_response.stream_to_file(str(speech_file_path))
        playsound.playsound(str(speech_file_path))
    except Exception as e:
        print("An error occurred in text-to-speech:", e)

# Initialize OpenAI client
client = openai.OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# Voice recognition
speech_text = recognize_speech_from_mic()
print("Recognized Speech:", speech_text)

# Get response from OpenAI
openai_response = get_response_from_openai(speech_text, client)
print("OpenAI Response:", openai_response)

# Convert response to speech
text_to_speech(openai_response, client)
