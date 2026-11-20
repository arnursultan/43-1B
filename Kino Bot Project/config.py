import os
from pathlib import Path

from dotenv import load_dotenv

load_dotenv()

TOKEN = os.getenv("BOT_TOKEN")
WEBHOOK_SECRET = os.getenv("WEBHOOK_SECRET")
DEFAULT_DB_PATH = "/tmp/kino.db" if os.getenv("VERCEL") else str(Path(__file__).resolve().parent / "kino.db")
DB_PATH = os.getenv("DB_PATH", DEFAULT_DB_PATH)
