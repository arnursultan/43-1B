from aiogram import F, Router
from aiogram.filters import Command, CommandStart
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, Message

from database import Database
from keyboards import main_menu

router = Router()

DEMO = [
    ("Бриллиантовая рука", "😂 Комедия", 5),
    ("Шрек", "🧸 Мульт", 4),
    ("Интерстеллар", "🚀 Фантастика", 5),
    ("Один дома", "😂 Комедия", 4),
    ("Начало", "🚀 Фантастика", 5),
    ("Крик" "😱 Ужасы", 2),
    ("Джон Уик", "💥 Боевик", 4),
]

@router.message(CommandStart())
async def cmd_start(message: Message, state: FSMContext):
    await state.clear()
    await message.answer(
        "🍿 <b>Кино-Клуб Открыт!</b>\n"
        "Складывай фильмы в кинотеку, а я скажу, что смотреть сегодня вечером.\n"
        "Меню внизу 👇🏻",
        reply_markup=main_menu,
    )

@router.message(Command("cancel"))
async def cmd_cancel(message: Message, state: FSMContext):
    await state.clear()
    await message.answer("❌")
