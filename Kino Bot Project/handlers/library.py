from math import ceil

from aiogram import F, Router
from aiogram.exceptions import TelegramBadRequest
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, Message

from database import Database
from keyboards import (
    BTN_LIST, BTN_RANDOM, PAGE_SIZE, Act, OpenFilm, Page,
    card_kb, confirm_delete_kb, films_kb, pick_kb,
)
from texts import EMPTY, card_text

router = Router()


def list_view(db: Database, user_id: int, page: int):
    total = db.count_films(user_id)
    if total == 0:
        return EMPTY, None
    pages = ceil(total / PAGE_SIZE)
    page = max(0, min(page, pages - 1))
    films = db.list_films(user_id, page * PAGE_SIZE, PAGE_SIZE)
    return f"📋 <b>Твоя кинотека</b>: {total} шт.\nТыкай на фильм 👇", films_kb(films, page, pages)


def pick_view(db: Database, user_id: int):
    film = db.random_unwatched(user_id)
    if film is None:
        return "🤷 Смотреть нечего: всё уже просмотрено (или кинотека пуста).", None
    return "🎲 <b>Сегодня смотрим:</b>\n\n" + card_text(film), pick_kb(film)


async def show(callback: CallbackQuery, text: str, kb=None):
    try:
        await callback.message.edit_text(text, reply_markup=kb)
    except TelegramBadRequest as e:
        if "message is not modified" not in str(e):
            raise


async def film_or_bounce(callback: CallbackQuery, db: Database, film_id: int, page: int):
    film = db.get_film(callback.from_user.id, film_id)
    if film is None:
        await callback.answer("Этого фильма уже нет 🤷", show_alert=True)
        text, kb = list_view(db, callback.from_user.id, page)
        await show(callback, text, kb)
    return film


@router.message(F.text == BTN_LIST)
async def menu_list(message: Message, state: FSMContext, db: Database):
    await state.clear()
    text, kb = list_view(db, message.from_user.id, 0)
    await message.answer(text, reply_markup=kb)


@router.message(F.text == BTN_RANDOM)
async def menu_random(message: Message, state: FSMContext, db: Database):
    await state.clear()
    text, kb = pick_view(db, message.from_user.id)
    await message.answer(text, reply_markup=kb)


@router.callback_query(Page.filter())
async def go_page(callback: CallbackQuery, callback_data: Page, db: Database):
    if callback_data.n < 0:
        await callback.answer("Это первая страница")
        return
    text, kb = list_view(db, callback.from_user.id, callback_data.n)
    await show(callback, text, kb)
    await callback.answer()


@router.callback_query(OpenFilm.filter())
async def open_film(callback: CallbackQuery, callback_data: OpenFilm, db: Database):
    film = await film_or_bounce(callback, db, callback_data.id, callback_data.page)
    if film is None:
        return
    await show(callback, card_text(film), card_kb(film, callback_data.page))
    await callback.answer()


@router.callback_query(F.data == "random")
async def another_pick(callback: CallbackQuery, db: Database):
    text, kb = pick_view(db, callback.from_user.id)
    await show(callback, text, kb)
    await callback.answer()


@router.callback_query(Act.filter(F.action == "watch"))
async def toggle_watched(callback: CallbackQuery, callback_data: Act, db: Database):
    film = await film_or_bounce(callback, db, callback_data.id, callback_data.page)
    if film is None:
        return
    db.set_watched(callback.from_user.id, film["id"], not film["watched"])
    film = db.get_film(callback.from_user.id, film["id"])
    await show(callback, card_text(film), card_kb(film, callback_data.page))
    await callback.answer("Готово 👌")


@router.callback_query(Act.filter(F.action == "hype"))
async def set_hype(callback: CallbackQuery, callback_data: Act, db: Database):
    if not 1 <= callback_data.v <= 5:
        await callback.answer("Некорректная оценка", show_alert=True)
        return
    film = await film_or_bounce(callback, db, callback_data.id, callback_data.page)
    if film is None:
        return
    if film["hype"] == callback_data.v:
        await callback.answer("Уже стоит столько 🙂")
        return
    db.set_hype(callback.from_user.id, film["id"], callback_data.v)
    film = db.get_film(callback.from_user.id, film["id"])
    await show(callback, card_text(film), card_kb(film, callback_data.page))
    await callback.answer("Ажиотаж обновлён 🔥")


@router.callback_query(Act.filter(F.action == "del"))
async def ask_delete(callback: CallbackQuery, callback_data: Act, db: Database):
    film = await film_or_bounce(callback, db, callback_data.id, callback_data.page)
    if film is None:
        return
    await show(callback, f"🗑 Удалить «{film['title']}»? Обратно не вернёшь.", confirm_delete_kb(film, callback_data.page))
    await callback.answer()


@router.callback_query(Act.filter(F.action == "delok"))
async def do_delete(callback: CallbackQuery, callback_data: Act, db: Database):
    deleted = db.delete_film(callback.from_user.id, callback_data.id)
    await callback.answer("Удалено 🪦" if deleted else "Уже удалено", show_alert=not deleted)
    text, kb = list_view(db, callback.from_user.id, callback_data.page)
    await show(callback, text, kb)
