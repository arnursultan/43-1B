from aiogram import Router
from aiogram.filters import Command, CommandStart
from aiogram.types import Message

import stats

router = Router()

@router.message(CommandStart())
async def start(message: Message):
    stats.users.add(message.from_user.id)
    await message.answer(
        "🕹️ <b>Аркада открыта!<b>\n"
        "Йоу, Кидай эмодзи 🎲 🎰 ⚽️ 🏈 🏀 🎳 🎯 — или чекни команды: /help"
    )

@router.message(Command("help"))
async def help(message: Message):
    await message.answer(
        "<b>Что умеет бот:<b>\n"
        "🎮 /dice /darts /basket /football /bowling /slots — играет бот.\n"
        "🎰 или просто пришли в чат эмодзи ⚽️ / 🎳 / 🎯 — сыграешь сам.\n"
        "🌸 /luck — твоя удача на сегодня\n"
        "📸 Пришли стикер или фото — я отреагирую\n"
        "🔮 Задай вопрос — отвечу как аля-магический шар\n"
        "🆔 /id — твой Telegram ID"
    )

@router.message(Command("id"))
async def id(message: Message):
    await message.answer(
        f"🆔 Твой ID: <code>{message.from_user.id}</code>"
    )
