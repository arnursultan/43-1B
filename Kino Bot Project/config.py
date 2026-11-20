import os
from pathlib import Path

from dotenv import load_dotenv

load_dotenv()

TOKEN = os.getenv("BOT_TOKEN")
WEBHOOK_SECRET = os.getenv("WEBHOOK_SECRET")
DB_PATH = os.getenv("DB_PATH", str(Path(__file__).resolve().parent / "kino.db"))
