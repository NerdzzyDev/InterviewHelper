# → voice_handler.py
import base64
import io
import sounddevice as sd
import soundfile as sf
import numpy as np
import threading
from pynput import keyboard
import google.generativeai as genai
from config import API_KEY

genai.configure(api_key=API_KEY, transport='rest')

is_recording = False
audio_data = []
stream = None
alt_pressed = False

def get_default_microphone():
    device = sd.default.device[0]
    print(f"🎤 Используется: {sd.query_devices(device)['name']}")
    return device

def start_recording():
    global is_recording, audio_data, stream
    if is_recording:
        return
    print("🔴 Запись началась (Alt+Z для остановки)")
    audio_data = []
    is_recording = True

    def callback(indata, frames, time, status):
        if is_recording:
            audio_data.append(indata.copy())

    stream = sd.InputStream(device=get_default_microphone(), samplerate=44100, channels=1, dtype='float32', callback=callback)
    stream.start()
    threading.Timer(10.0, stop_recording).start()

def stop_recording():
    global is_recording, stream
    if not is_recording:
        return
    is_recording = False
    if stream:
        stream.stop()
        stream.close()
    if audio_data:
        full_audio = np.concatenate(audio_data)
        audio_buffer = io.BytesIO()
        sf.write(audio_buffer, full_audio, 44100, format="WAV")
        transcribe_audio(audio_buffer.getvalue())
    else:
        print("❌ Нет звуковых данных")

def transcribe_audio(audio_bytes):
    try:
        model = genai.GenerativeModel('gemini-2.0-flash')
        audio_base64 = base64.b64encode(audio_bytes).decode("utf-8")
        response = model.generate_content([
            "Это собеседование по Python. Определи вопрос, дай краткий ответ и объясни:",
            {"mime_type": "audio/wav", "data": audio_base64}
        ], stream=False) # заменить на True

        print("\n🔊 Ответ от Gemini:")
        for chunk in response:
            if hasattr(chunk, 'text') and chunk.text:
                print(chunk.text)
    except Exception as e:
        print(f"❌ Ошибка: {e}")

def on_press(key):
    global alt_pressed
    if key in {keyboard.Key.alt, keyboard.Key.alt_l, keyboard.Key.alt_r}:
        alt_pressed = True
    if hasattr(key, 'char') and key.char == 'z' and alt_pressed:
        if is_recording:
            stop_recording()
        else:
            start_recording()

def on_release(key):
    global alt_pressed
    if key in {keyboard.Key.alt, keyboard.Key.alt_l, keyboard.Key.alt_r}:
        alt_pressed = False

def run_voice_assistant():
    print("🎙️ Голосовой ассистент запущен. Alt+Z для записи")
    with keyboard.Listener(on_press=on_press, on_release=on_release) as listener:
        listener.join()
