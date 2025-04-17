import speech_recognition as sr
import requests
from gtts import gTTS
from pydub import AudioSegment
from pydub.playback import play
import os

# URL to your local Rasa server
RASA_ENDPOINT = "http://localhost:5005/webhooks/rest/webhook"

def listen_from_mic():
    recognizer = sr.Recognizer()
    mic = sr.Microphone()

    with mic as source:
        print("🎤 பேசுங்கள்...")
        recognizer.adjust_for_ambient_noise(source)
        audio = recognizer.listen(source)

    try:
        user_input = recognizer.recognize_google(audio, language='ta-IN')
        print(f"👤 நீங்கள் சொன்னது: {user_input}")
        return user_input
    except sr.UnknownValueError:
        print("🤖 உரையை புரிந்துகொள்ள முடியவில்லை.")
        return None
    except sr.RequestError as e:
        print("⚠️ Google Speech API பிழை:", e)
        return None

def send_to_rasa(text):
    payload = {"sender": "user", "message": text}
    try:
        response = requests.post(RASA_ENDPOINT, json=payload)
        if response.ok and response.json():
            return response.json()[0]['text']
        else:
            return "மன்னிக்கவும், பதில் பெற முடியவில்லை."
    except requests.exceptions.RequestException:
        return "Rasa சேவையை அணுக முடியவில்லை."

def speak_tamil(text):
    tts = gTTS(text=text, lang='ta')
    tts.save("response.mp3")
    audio = AudioSegment.from_mp3("response.mp3")
    play(audio)
    os.remove("response.mp3")

def main():
    print("📞 தமிழ் டெலிகாலிங் AI உதவியாளர் தயாராக இருக்கிறார்!")
    speak_tamil("வணக்கம்! உங்கள் கேள்வியை கூறுங்கள்.")

    while True:
        input("▶️ பேச தொடங்க Enter ஐ அழுத்தவும்...")

        user_input = listen_from_mic()
        if user_input:
            if any(stop_word in user_input.lower() for stop_word in ["நிறுத்து", "வணக்கம்", "exit", "stop"]):
                speak_tamil("நன்றி! மீண்டும் சந்திப்போம்.")
                break

            rasa_reply = send_to_rasa(user_input)
            print(f"🤖 பதில்: {rasa_reply}")
            speak_tamil(rasa_reply)
        else:
            speak_tamil("தயவுசெய்து மீண்டும் முயற்சிக்கவும்.")

if __name__ == "__main__":
    main()
