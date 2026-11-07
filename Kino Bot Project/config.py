import os

from dotenv import load_dotenv

load_dotenv()

TOKEN = os.getenv("BOT_TOKEN")
if not TOKEN:
    raise SystemExit("❌ Токен не найден. Проверьте файл .env")

DB_PATH = os.getenv("DB_PATH", "kino.db")
