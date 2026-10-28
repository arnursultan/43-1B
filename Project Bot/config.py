import os

from dotenv import load_dotenv

load_dotenv()

TOKEN = os.getenv("BOT_TOKEN")
if not TOKEN:
    raise SystemExit("Токен не найден. Проверьте .env, а именно строка BOT_TOKEN=...")