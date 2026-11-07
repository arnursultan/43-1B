from aiogram.fsm.state import State, StatesGroup

class AddFilm(StatesGroup):
    title = State()
    genre = State()
    hype = State()

class Rename(StatesGroup):
    title = State()