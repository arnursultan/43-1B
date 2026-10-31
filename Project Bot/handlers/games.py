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

]

# git init
# git add .
# git commit -m "Lesson 4"
# git branch -M main
# git remote add origin linkgithub.com
# git push -u origin main