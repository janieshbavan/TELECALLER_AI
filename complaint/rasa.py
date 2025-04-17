import speech_recognition as sr
import requests
from gtts import gTTS
import os
import playsound

# Rasa local server endpoint
RASA_URL = "http://localhost:5005/webhooks/rest/webhook"

def get_speech_input():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print("\n🎤 Speak now...")
        recognizer.adjust_for_ambient_noise(source)
        audio = recognizer.listen(source)
    try:
        text = recognizer.recognize_google(audio)
        print(f"🗣️ You: {text}")
        return text
    except sr.UnknownValueError:
        print("🤷 Couldn't understand what you said.")
        return None
    except sr.RequestError as e:
        print(f"❌ Speech recognition error: {e}")
        return None

def query_rasa(text):
    payload = {"sender": "user", "message": text}
    try:
        response = requests.post(RASA_URL, json=payload)
        if response.status_code == 200:
            replies = response.json()
            if replies:
                return replies[0]['text']
    except Exception as e:
        print(f"⚠️ Error communicating with Rasa: {e}")
    return "Sorry, I couldn't reach the bot."

def speak_text(text):
    tts = gTTS(text=text, lang='en')
    file = "response.mp3"
    tts.save(file)
    playsound.playsound(file)
    os.remove(file)

def main():
    print("🤖 Speak to the bot! (Say 'stop' to exit)")
    while True:
        user_input = get_speech_input()
        if not user_input:
            continue
        if user_input.lower() == "stop":
            print("👋 Chat ended.")
            break
        bot_reply = query_rasa(user_input)
        print(f"🤖 Bot: {bot_reply}")
        speak_text(bot_reply)

if __name__ == "__main__":
    main()
