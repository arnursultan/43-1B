import html

HYPE_TEXT = {
    1: "может, когда-нибудь",
    2: "можно, если больше нечего делать",
    3: "норм, гляну фильм",
    4: "неплохо, стоит глянуть",
    5: "СМОТРЕТЬ СЕГОДНЯ ИЛИ УМРУ",
}

EMPTY = "🎬 Кинотека пуст, как холодильник в конце месяца.\nНажми «➕ Добавить фильм» (или отправь /demo для тестовых."

def card_text(film) -> str:
    status = "✅ Посмотрел. Мнение иметь разрешено." if film["watched"] else "🍿 В очереди"
    return (
        f"🎥 <b>{html.escape(film['title'])}</b>\n"
        f"{html.escape(film['genre'])}\n"
        f"🔥 Ажиотаж: {film['hype']}/5 — {HYPE_TEXT[film['hype']]}\n"
        f"{status}"
    )
