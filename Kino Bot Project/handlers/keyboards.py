from aiogram.types import InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder, ReplyKeyboardBuilder

from texts import HYPE_TEXT

GENRES = ["😂 Комедия", "💥 Боевик", "😱 Ужасы", "🚀 Фантастика", "🎭 Драма", "🧸 Мульт"]
PAGE_SIZE = 5

BTN_ADD = "➕ Добавить фильм"
BTN_LIST = "📋 Мои фильмы"
BTN_RANDOM = "🎲 Что смотреть?"


class OpenFilm(CallbackData, prefix="film"):
    id: int
    page: int

class Page(CallbackData, prefix="page"):
    n: int

class Act(CallbackData, prefix="act"):
    action: str
    id: int
    page: int = 0
    v: int = 0

class GenrePick(CallbackData, prefix="genre"):
    i: int

class HypePick(CallbackData, prefix="hype"):
    v: int

def main_menu():
    builder = ReplyKeyboardBuilder()
    builder.button(text=BTN_ADD)
    builder.button(text=BTN_LIST)
    builder.button(text=BTN_RANDOM)
    builder.adjust(1, 2)
    return builder.as_markup(resize_keyboard=True, input_field_placeholder="Выбери в меню 👇")

def films_kb(films, page: int, pages: int):
    builder = InlineKeyboardBuilder()
    for f in films:
        icon = "✅" if f["watched"] else "🍿"
        builder.button(text=f"{icon} {f['title']}", callback_data=OpenFilm(id=f["id"], page=page))
    sizes = [1] * len(films)

    nav = 0
    if page > 0:
        builder.button(text="⬅️", callback_data=Page(n=page - 1))
        nav += 1
    if pages > 1:
        builder.button(text=f"{page + 1}/{pages}", callback_data="noop")
        nav += 1
    if page < pages - 1:
        builder.button(text="➡️", callback_data=Page(n=page + 1))
        nav += 1
    if nav:
        sizes.append(nav)
    builder.adjust(*sizes)
    return builder.as_markup()

def card_kb(film, page: int):
    builder = InlineKeyboardBuilder()
    watch_text = "↩️ Не смотрел" if film["watched"] else "✅ Посмотрел"
    builder.button(text=watch_text, callback_data=Act(action="watch", id=film["id"], page=page))
    for n in range(1, 6):
        builder.button(
            text="🔥" if n == film["hype"] else str(n),
            callback_data=Act(action="hype", id=film["id"], page=page, v=n),
        )
    builder.button(text="🗑 Удалить", callback_data=Act(action="del", id=film["id"], page=page))
    builder.button(text="⬅️ К списку", callback_data=Page(n=page))
    builder.adjust(1, 5, 1, 1)
    return builder.as_markup()

def confirm_delete_kb(film, page: int):
    builder = InlineKeyboardBuilder()
    builder.button(text="✅ Да, удалить", callback_data=Act(action="delok", id=film["id"], page=page))
    builder.button(text="↩️ Нет", callback_data=OpenFilm(id=film["id"], page=page))
    builder.adjust(2)
    return builder.as_markup()

def pick_kb(film):
    builder = InlineKeyboardBuilder()
    builder.button(text="📖 Открыть", callback_data=OpenFilm(id=film["id"], page=0))
    builder.button(text="🎲 Другой", callback_data="random")
    builder.adjust(2)
    return builder.as_markup()

def genre_kb():
    builder = InlineKeyboardBuilder()
    for i, genre in enumerate(GENRES):
        builder.button(text=genre, callback_data=GenrePick(i=i))
    builder.adjust(2)
    builder.row(InlineKeyboardButton(text="❌ Отмена", callback_data="cancel"))
    return builder.as_markup()

def hype_kb():
    builder = InlineKeyboardBuilder()
    for n in range(1, 6):
        builder.button(text=f"{n} · {HYPE_TEXT[n]}", callback_data=HypePick(v=n))
    builder.button(text="❌ Отмена", callback_data="cancel")
    builder.adjust(1)
    return builder.as_markup()