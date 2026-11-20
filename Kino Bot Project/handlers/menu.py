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
    ("Один дома", "😂 Комедия", 3),
    ("Начало", "🚀 Фантастика", 4),
    ("Крик", "😱 Ужасы", 2),
    ("Джон Уик", "💥 Боевик", 4),
]


@router.message(CommandStart())
async def cmd_start(message: Message, state: FSMContext):
    await state.clear()
    await message.answer(
        "🍿 <b>Кино-клуб открыт!</b>\n"
        "Складывай фильмы в кинотеку, а я скажу, что смотреть сегодня вечером.\n"
        "Меню внизу 👇",
        reply_markup=main_menu(),
    )


@router.message(Command("cancel"))
async def cmd_cancel(message: Message, state: FSMContext):
    await state.clear()
    await message.answer("❌ Отменено. Забыли, как страшный сон.", reply_markup=main_menu())


@router.callback_query(F.data == "cancel")
async def cancel_button(callback: CallbackQuery, state: FSMContext):
    await state.clear()
    await callback.message.edit_text("❌ Отменено.")
    await callback.answer()


@router.callback_query(F.data == "noop")
async def noop(callback: CallbackQuery):
    await callback.answer()


@router.message(Command("demo"))
async def cmd_demo(message: Message, db: Database):
    added = sum(db.add_film(message.from_user.id, t, g, h) is not None for t, g, h in DEMO)
    await message.answer(f"🍿 Добавлено фильмов: {added}. Жми «📋 Мои фильмы».")
