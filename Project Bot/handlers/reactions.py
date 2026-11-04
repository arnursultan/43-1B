import html
import random

from aiogram import F, Router
from aiogram.types import Message

router = Router()

PHOTO_NOTES = [
    "Не хватает кота.",
    "Слишком много света, слишком мало смысла.",
    "Пятёрка за старание.",
    "Not bad."
]

BALL = [
    "Да, 100%",
    "Определённо нет.",
    "Спроси у мамы.",
    "Звёзды говорят «может быть»",
    "Даже не думай.",
    "Домой Уолтер."
]

@router.message(F.photo & F.caption)
async def photo_with_caption(message: Message):
    await message.reply(
        f"📸 Подпись «{html.escape(message.caption)}» — сильно. "
        f"Фото: {random.randint(3, 10)}/10."
    )

@router.message(F.photo)
async def photo(message: Message):
    await message.reply(f"📸 Принято. Оценка: {random.randint(3, 10)}/10. {random.choice(PHOTO_NOTES)}")

@router.message(F.sticker)
async def sticker(message: Message):
    await message.answer("🔄 Reverse! Держи свой стикер обратно:")
    await message.answer_sticker(message.sticker.file_id)

@router.message(F.voice | F.video_note)
async def voice(message: Message):
    await message.reply("🎙 Голосовые и кружочки не принимаю. Я бот, мне некогда. Пиши текстом, гений.")

@router.message(F.text.lower().in_({"привет", "здарова", "хай", "ку", "hi", "sup", "hello"}))
async def hello(message: Message):
    await message.answer("👋🏼 Салют! Кидай 🎲 или кликай /help")

@router.message(F.text.endswith("?"))
async def magic_ball(message: Message):
    await message.reply(f"🔮 {random.choice(BALL)}")


