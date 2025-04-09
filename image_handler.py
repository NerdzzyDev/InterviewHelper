# → image_handler.py
import base64
import subprocess
import time
import threading
import google.generativeai as genai
from config import API_KEY


genai.configure(api_key=API_KEY, transport='rest')

def send_image_to_gemini(image_bytes):
    try:
        model = genai.GenerativeModel('gemini-1.5-pro')
        image_base64 = base64.b64encode(image_bytes).decode("utf-8")
        response = model.generate_content([
            "Распознай текст на изображении и опиши, что на нём видно:",
            {"mime_type": "image/png", "data": image_base64}
        ], stream=True)

        print("\n🖼 Ответ от Gemini:")
        for chunk in response:
            if hasattr(chunk, 'text') and chunk.text:
                print(chunk.text)

    except Exception as e:
        print(f"❌ Ошибка при обработке изображения: {e}")

def check_clipboard():
    last_clipboard = None
    while True:
        clipboard_data = subprocess.run(["wl-paste", "--type", "text"], capture_output=True, text=True).stdout.strip()
        if clipboard_data != last_clipboard:
            if clipboard_data == "":
                clipboard_image = subprocess.run(["wl-paste", "--type", "image/png"], capture_output=True)
                if clipboard_image.stdout:
                    send_image_to_gemini(clipboard_image.stdout)
            last_clipboard = clipboard_data
        time.sleep(1)

def run_clipboard_monitor():
    threading.Thread(target=check_clipboard, daemon=True).start()
    print("🧪 Отслеживание буфера обмена запущено...")
