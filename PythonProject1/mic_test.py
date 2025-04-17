import whisper
import sounddevice as sd
from scipy.io.wavfile import write
import tempfile

# Record audio
def record_audio(duration=5, fs=16000):
    print("🎙️ Recording started... Speak now!")
    audio = sd.rec(int(duration * fs), samplerate=fs, channels=1, dtype='int16')
    sd.wait()
    print("✅ Recording complete.")
    return fs, audio

# Save to a temporary file
def save_to_wav(fs, audio):
    temp_file = tempfile.NamedTemporaryFile(suffix=".wav", delete=False)
    write(temp_file.name, fs, audio)
    return temp_file.name

# Transcribe using Whisper
def transcribe_from_mic(language="ta"):
    fs, audio = record_audio()
    wav_path = save_to_wav(fs, audio)

    model = whisper.load_model("base")
    result = model.transcribe(wav_path, language=language)
    print("🗣️ You said:", result["text"])

# Run the transcription
transcribe_from_mic()
