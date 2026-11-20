import hmac
import json
import logging
from pathlib import Path
import sys

from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.types import Update
from fastapi import FastAPI, HTTPException, Request, Response

PROJECT_DIR = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PROJECT_DIR))

import config
from database import Database
from handlers import add_film, fallback, library, menu

logging.basicConfig(level=logging.INFO)

app = FastAPI(docs_url=None, redoc_url=None)
bot = Bot(token=config.TOKEN or "", default=DefaultBotProperties(parse_mode=ParseMode.HTML))
dispatcher = Dispatcher()
dispatcher.include_routers(menu.router, library.router, add_film.router, fallback.router)


@app.get("/")
async def healthcheck():
    return {"status": "ok"}


@app.post("/api/webhook")
async def telegram_webhook(request: Request):
    if not config.TOKEN or not config.WEBHOOK_SECRET:
        raise HTTPException(status_code=503, detail="Webhook is not configured")

    supplied_secret = request.headers.get("X-Telegram-Bot-Api-Secret-Token", "")
    if not hmac.compare_digest(supplied_secret, config.WEBHOOK_SECRET):
        raise HTTPException(status_code=403, detail="Forbidden")

    try:
        payload = await request.json()
        update = Update.model_validate(payload, context={"bot": bot})
    except (json.JSONDecodeError, ValueError) as exc:
        raise HTTPException(status_code=400, detail="Invalid Telegram update") from exc

    db = Database(config.DB_PATH)
    try:
        await dispatcher.feed_update(bot, update, db=db)
    finally:
        db.close()

    return Response(status_code=200)
