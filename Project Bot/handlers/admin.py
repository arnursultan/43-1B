from aiogram import F, Router
from aiogram.filters import Command
from aiogram.types import Message

import stats
from custom_filters import IsAdmin

router = Router()
router.message.filter(F.chat.type == "private")

@router.message(Command("stats"), IsAdmin())
async def show_stats(message: Message):
    rows = "\n".join(f"{emoji} x {n}" for emoji, n in stats.plays.most_common() or "пока тишина")
    await message.answer(
        f"📊 <b>Статистика всея базы<b>\n"
        f"Игроков: {len(stats.users)}\n"
        f"Игр сыграно: {sum(stats.plays.values())}\n{rows}"
    )

@router.message(Command("stats"))
async def stats_denied(message: Message):
    await message.answer("🚫 Статистика только для админа. Ты пока не крут дружище. /id")