import speech_recognition as sr
import requests
from gtts import gTTS
from playsound import playsound
import os
import datetime

RASA_ENDPOINT = "http://localhost:5005/webhooks/rest/webhook"
COMPANY_NAME = "Excite Pvt Ltd"
COMPLAINT_FILE = "complaints.txt"

def listen_from_mic():
    recognizer = sr.Recognizer()
    mic = sr.Microphone()

    with mic as source:
        print("பேசுங்கள்...")
        recognizer.adjust_for_ambient_noise(source)
        audio = recognizer.listen(source)

    try:
        user_input = recognizer.recognize_google(audio, language='ta-IN')
        print(f"நீங்கள் சொன்னது: {user_input}")
        return user_input
    except sr.UnknownValueError:
        print("உங்களுடைய உரையை புரிந்துகொள்ள முடியவில்லை.")
        return None
    except sr.RequestError as e:
        print(" Google Speech API பிழை:", e)
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
    playsound("response.mp3")
    os.remove("response.mp3")

def register_complaint(complaint_text):
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with open(COMPLAINT_FILE, "a", encoding="utf-8") as f:
        f.write(f"[{timestamp}] Complaint registered for {COMPANY_NAME}: {complaint_text}\n")
    print(f"📄 புகார் பதிவு செய்யப்பட்டது: {complaint_text}")
    speak_tamil("உங்கள் புகார் பதிவு செய்யப்பட்டது. நன்றி!")

def main():
    print("தமிழ் டெலிகாலிங் AI உதவியாளர் தயாராக இருக்கிறார்!")
    speak_tamil("வணக்கம்! உங்கள் கேள்வியை கூறுங்கள்.")

    while True:
        input("▶️ பேச தொடங்க Enter ஐ அழுத்தவும்...")

        user_input = listen_from_mic()
        if user_input:
            # Complaint trigger
            if any(kw in user_input.lower() for kw in ["புகார்", "complaint", "சிக்கல்", "பிரச்சனை", "repair"]):
                register_complaint(user_input)
                continue

            # Exit trigger
            if any(stop_word in user_input.lower() for stop_word in ["நிறுத்து", "exit", "stop"]):
                speak_tamil("நன்றி! மீண்டும் சந்திப்போம்.")
                break

            # Default Rasa reply
            rasa_reply = send_to_rasa(user_input)
            print(f"🤖 பதில்: {rasa_reply}")
            speak_tamil(rasa_reply)
        else:
            speak_tamil("தயவுசெய்து மீண்டும் முயற்சிக்கவும்.")

if __name__ == "__main__":
    main()
    os.remove("response.mp3")
