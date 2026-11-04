import asyncio
import random
from datetime import date

from aiogram import F, Router
from aiogram.filters import Command, CommandObject
from aiogram.types import Message

import stats

router = Router()

GAMES = {
    "dice":     "🎲",
    "darts":    "🎯",
    "basket":   "🏀",
    "football": "⚽️",
    "bowling":  "🎳",
    "slots":    "🎰"
}

WIN = {
    "🎲": {6},
    "🎯": {6},
    "🏀": {4,5},
    "⚽️": {4,5},
    "🎳": {6},
    "🎰": {1,22,43,64}
}

WIN_TEXT = [
    "🏆 Победа! Лол-кек чебурек.",
    "🎉 Красавчик! Ты везунчик, бот в шоке и требует реванша."
    "🔥 Это было красиво. Я бы поаплодировал, но у меня нет рук."
]

LOSE_TEXT = [
    "💀 Мимо. Бывает. Нет, не бывает, но ты держись.",
    "🫠 Не повезло. Сделаем вид, что это лаги.",
    "📉 Проигрыш. Зато опыт, бесплатный.",
    "🪦 Press F. Минута молчания."
]

def verdict(emoji: str, value: int) -> str:
    if emoji == "🎰" and value == 64:
        return "🎰 ДЖЕКПОТ, три 777! Сегодня твой день!"
    return random.choice(WIN_TEXT if value in WIN[emoji] else LOSE_TEXT)

@router.message(Command(*GAMES))
async def play(message: Message, command: CommandObject):
    sent = await message.answer_dice(emoji=GAMES[command.command])
    await asyncio.sleep(3.5)
    stats.plays[sent.dice.emoji] += 1
    await message.answer(verdict(sent.dice.emoji, sent.dice.value))

@router.message(F.dice)
async def user_dice(message: Message):
    await asyncio.sleep(3.5)
    stats.plays[message.dice.emoji] += 1
    await message.reply(verdict(message.dice.emoji, message.dice.value))

@router.message(Command("luck"))
async def luck(message: Message):
    percent = random.Random(f"{message.from_user.id}-{date.today()}").randint(0, 100)
    if percent > 80:
        mood = "😎 Сегодня твой день, играй в 🎰"
    elif percent > 30:
        mood = "🙂‍↔️ Нормально. Не гений, не миллиардер и не лузер."
    else:
        mood = "☠️ Бро, лучше не выходи из дома. Приляг, поспи."
    await message.answer(f"Твоя удача на сегодня: <b>{percent}%</b>{mood}")