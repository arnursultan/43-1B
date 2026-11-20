import html

from aiogram import F, Router
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, Message

from database import Database
from keyboards import BTN_ADD, GENRES, GenrePick, HypePick, card_kb, genre_kb, hype_kb
from states import AddFilm
from texts import card_text

router = Router()

@router.message(F.text == BTN_ADD)
async def add_start(message: Message, state: FSMContext):
    await state.clear()
    await state.set_state(AddFilm.title)
    await message.answer("🎬 Как называется фильм?\nНапиши текстом. Передумал? Пиши: /cancel")

@router.message(AddFilm.title, F.text)
async def got_title(message: Message, state: FSMContext):
    title = message.text.strip()
    if not title:
        await message.answer("Название не должно быть пустым. Напиши название фильма.")
        return
    if title.startswith("/"):
        await message.answer("Это команда, а не фильм, гений 🧠 Напиши название или отмени /cancel")
        return
    if len(title) > 60:
        await message.answer("Длинновато: максимум 60 Символов. Алё, короче!")
        return
    await state.update_data(title=title)
    await state.set_state(AddFilm.genre)
    await message.answer("Жанр?", reply_markup=genre_kb())

@router.message(AddFilm.title)
async def title_not_text(message: Message):
    await message.answer("Мне нужен текст, Название фильма словами.")

@router.callback_query(AddFilm.genre, GenrePick.filter())
async def got_genre(callback:CallbackQuery, callback_data: GenrePick, state: FSMContext):
    if not 0 <= callback_data.i < len(GENRES):
        await callback.answer("Неизвестный жанр. Начни добавление заново.", show_alert=True)
        return
    genre = GENRES[callback_data.i]
    await state.update_data(genre=genre)
    await state.set_state(AddFilm.hype)
    await callback.message.edit_text(f"Жанр: {genre}\n\nНасколько хочешь посмотреть,", reply_markup=hype_kb())
    await callback.answer()

@router.message(AddFilm.genre)
async def genre_wants_button(message: Message):
    await message.answer("Жанр выбирают кнопками выше 👆 (или /cancel)")

@router.callback_query(AddFilm.hype, HypePick.filter())
async def got_hype(callback: CallbackQuery, callback_data: HypePick, state: FSMContext, db: Database):
    data = await state.get_data()
    await state.clear()
    film_id = db.add_film(callback.from_user.id, data["title"], data["genre"], callback_data.v)
    if film_id is None:
        await callback.message.edit_text(f"✋🏻 «{html.escape(data['title'])}» уже есть в твоей кинотеке.")
    else:
        film = db.get_film(callback.from_user.id, film_id)
        await callback.message.edit_text("✅ Добавлено!\n\n" + card_text(film), reply_markup=card_kb(film, 0))
    await callback.answer()

@router.message(AddFilm.hype)
async def hype_wants_button(message: Message):
    await message.answer("Ажиотаж выбирают кнопками выше 👆 (или /cancel)")



