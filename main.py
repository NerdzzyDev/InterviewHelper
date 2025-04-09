# 📁 project structure suggestion:
# project/
# ├── main.py
# ├── config.py
# ├── image_handler.py
# ├── voice_handler.py
# └── utils.py

# → main.py
from image_handler import run_clipboard_monitor
from voice_handler import run_voice_assistant
import time
import threading

if __name__ == "__main__":
    run_clipboard_monitor()
    threading.Thread(target=run_voice_assistant, daemon=True).start()
    while True:
        time.sleep(10)
