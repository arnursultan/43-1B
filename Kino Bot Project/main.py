# Keyboards
# 2 Основных вида клавиатур.

# ReplyKeyboardMarkup — Это клавиатура, которая появляется
# вместо обычной клавиатуры телефона.
# Например:
# — Мой профиль
# — Настройки
# — Помощь
# Когда пользователь нажимает кнопку, ТГ отправляет боту обычный текст.

# InlineKeyboardMarkup — Это кнопки непосредственно под сообщением бота.
# Например:
# — Открыть профиль
# — Удалить задачу
# — Подтвердить товар

# Inline позволяет взаимодействовать с конкретным сообщением.

# CallbackQuery — Это механизм обработки нажатий на inline кнопки
# Например:
# Пользователь нажимает "Удалить Задачу"..
# Бот получает CallbackQuery и понимает, какую именно кнопку нажал пользователь.

# FSM - Finite State Machine — Конечный автомат событий.
# Бот запоминает, какой вопрос он сейчас задаёт пользователю и какой ответ ожидает.


import asyncio
import logging

from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.types import BotCommand

import config
from database import Database
from handlers import add_film, fallback, library, menu


async def main():
    if not config.TOKEN:
        raise RuntimeError("BOT_TOKEN не задан")
    logging.basicConfig(level=logging.INFO)
    db = Database(config.DB_PATH)
    bot = Bot(token=config.TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))

    dp = Dispatcher(db=db)

    dp.include_routers(menu.router, library.router, add_film.router, fallback.router)

    try:
        await bot.set_my_commands([
            BotCommand(command="start", description="Открыть меню"),
            BotCommand(command="cancel", description="Отменить диалог"),
            BotCommand(command="demo", description="Добавить тестовые фильмы"),
        ])
        await dp.start_polling(bot)
    finally:
        db.close()
        await bot.session.close()


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\n👋 Сеанс окончен. Попкорн не забудь убрать.")
