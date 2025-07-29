# import speech_recognition as sr

# def listen_for_trigger(trigger_phrases=None, timeout=5):
#     if trigger_phrases is None:
#         trigger_phrases = ["describe", "describe the scene", "what do you see", "scene", "dekho"]

#     recognizer = sr.Recognizer()
#     mic = sr.Microphone()

#     print("🎤 Listening for voice command...")

#     with mic as source:
#         recognizer.adjust_for_ambient_noise(source)
#         try:
#             audio = recognizer.listen(source, timeout=timeout)
#             command = recognizer.recognize_google(audio).lower()
#             print(f"🔊 Heard: {command}")
#             for trigger in trigger_phrases:
#                 if trigger in command:
#                     return True
#         except sr.WaitTimeoutError:
#             print("⌛ Listening timed out.")
#         except sr.UnknownValueError:
#             print("❌ Could not understand the audio.")
#         except sr.RequestError as e:
#             print(f"❌ Speech Recognition error: {e}")
    
#     return False

# This replaces your existing listen.py file using offline speech recognition:
# scene_description/listen_vosk.py
import queue
import sounddevice as sd
import sys
import json
from vosk import Model, KaldiRecognizer
import os
base_dir = os.path.dirname(os.path.abspath(__file__))
MODEL_PATH = os.path.join(base_dir, "..", "vosk-model-small-en-in-0.4")

# Load model
# MODEL_PATH = "vosk_models/vosk-model-small-en-us-0.15"
# MODEL_PATH = "vosk-model-small-en-in-0.4"

model = Model(MODEL_PATH)
print("📁 Loading Vosk model from:", MODEL_PATH)

# Create a streaming recognizer
recognizer = KaldiRecognizer(model, 16000)
audio_queue = queue.Queue()

def audio_callback(indata, frames, time, status):
    if status:
        print(f"⚠️ Audio status: {status}", file=sys.stderr)
    audio_queue.put(bytes(indata))

def listen_for_command():
    print("🎤 Listening for command (Vosk)...")
    with sd.RawInputStream(samplerate=16000, blocksize=8000, dtype='int16',
                           channels=1, callback=audio_callback):
        while True:
            data = audio_queue.get()
            if recognizer.AcceptWaveform(data):
                result = recognizer.Result()
                text = json.loads(result).get("text", "")
                if text:
                    print(f"✅ Heard: {text}")
                    return text
