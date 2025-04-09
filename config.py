import os
from dotenv import load_dotenv

# Загрузка переменных окружения из файла .env
load_dotenv()

# Получение значений из переменных окружения
API_KEY = os.getenv("API_KEY")
PROXY_IP = os.getenv("PROXY_IP")
PROXY_PORT = os.getenv("PROXY_PORT")
PROXY_LOGIN = os.getenv("PROXY_LOGIN")
PROXY_PASSWORD = os.getenv("PROXY_PASSWORD")

# Формирование URL прокси с аутентификацией
PROXY_URL = f"socks5h://{PROXY_LOGIN}:{PROXY_PASSWORD}@{PROXY_IP}:{PROXY_PORT}"

# Установка переменных окружения
os.environ["HTTP_PROXY"] = PROXY_URL
os.environ["HTTPS_PROXY"] = PROXY_URL

# Проверка, что переменные загружены (опционально)
if not API_KEY:
    print("API_KEY не найден в файле .env")
if not PROXY_IP:
    print("PROXY_IP не найден в файле .env")