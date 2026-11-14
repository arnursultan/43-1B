from aiogram import Router
from aiogram.types import CallbackQuery, Message

from keyboards import main_menu

router = Router()

@router.message()
async def fallback_message(message: Message):
    await message.answer("🤷🏻 Не понял. Открой меню внизу 👇🏻", reply_markup=main_menu())

@router.callback_query()
async def fallback_callback(callback: CallbackQuery):
    await callback.answer("Дружище, кнопка устарела. Начни заново через меню 👇🏻", show_alert=True)