import openai
from gtts import gTTS
import os
import playsound
import speech_recognition as sr

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

def get_response_from_openai(text):
    client = openai.OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
    response = client.chat.completions.create(
        messages=[{"role": "user", "content": text}],
        model="gpt-4"
    )
    return response.choices[0].message.content

def text_to_speech(text):
    tts = gTTS(text=text, lang='en')
    filename = 'temp_audio.mp3'
    tts.save(filename)
    playsound.playsound(filename)
    os.remove(filename)

# Voice recognition
speech_text = recognize_speech_from_mic()
print("Recognized Speech:", speech_text)

# Get response from OpenAI
openai_response = get_response_from_openai(speech_text)
print("OpenAI Response:", openai_response)

# Convert response to speech
text_to_speech(openai_response)
