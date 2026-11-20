import random
import sqlite3


class Database:
    def __init__(self, path: str):
        self.conn = sqlite3.connect(path)
        self.conn.row_factory = sqlite3.Row
        self._create_tables()

    def close(self):
        self.conn.close()

    def _create_tables(self):
        with self.conn:
            self.conn.execute(
                """
                CREATE TABLE IF NOT EXISTS films (
                    id        INTEGER PRIMARY KEY AUTOINCREMENT,
                    user_id   INTEGER NOT NULL,
                    title     TEXT    NOT NULL,
                    title_key TEXT    NOT NULL,
                    genre     TEXT    NOT NULL,
                    hype      INTEGER NOT NULL DEFAULT 3 CHECK (hype BETWEEN 1 AND 5),
                    watched   INTEGER NOT NULL DEFAULT 0,
                    UNIQUE (user_id, title_key)
                )
                """
            )

    def add_film(self, user_id: int, title: str, genre: str, hype: int) -> int | None:
        title = title.strip()
        if not title or not genre or not 1 <= hype <= 5:
            raise ValueError("Название, жанр и ажиотаж 1–5 обязательны")
        try:
            with self.conn:
                cur = self.conn.execute(
                    "INSERT INTO films (user_id, title, title_key, genre, hype) VALUES (?, ?, ?, ?, ?)",
                    (user_id, title, title.casefold(), genre, hype),
                )
        except sqlite3.IntegrityError:
            return None
        return cur.lastrowid

    def get_film(self, user_id: int, film_id: int):
        return self.conn.execute(
            "SELECT * FROM films WHERE id = ? AND user_id = ?", (film_id, user_id)
        ).fetchone()

    def count_films(self, user_id: int) -> int:
        return self.conn.execute("SELECT COUNT(*) FROM films WHERE user_id = ?", (user_id,)).fetchone()[0]

    def list_films(self, user_id: int, offset: int, limit: int):
        return self.conn.execute(
            "SELECT * FROM films WHERE user_id = ? ORDER BY watched, id DESC LIMIT ? OFFSET ?",
            (user_id, limit, offset),
        ).fetchall()

    def random_unwatched(self, user_id: int):
        rows = self.conn.execute(
            "SELECT * FROM films WHERE user_id = ? AND watched = 0", (user_id,)
        ).fetchall()
        if not rows:
            return None
        return random.choices(rows, weights=[r["hype"] for r in rows])[0]

    def set_watched(self, user_id: int, film_id: int, watched: bool) -> bool:
        with self.conn:
            cur = self.conn.execute(
                "UPDATE films SET watched = ? WHERE id = ? AND user_id = ?", (int(watched), film_id, user_id)
            )
        return cur.rowcount > 0

    def set_hype(self, user_id: int, film_id: int, hype: int) -> bool:
        if not 1 <= hype <= 5:
            return False
        with self.conn:
            cur = self.conn.execute(
                "UPDATE films SET hype = ? WHERE id = ? AND user_id = ?", (hype, film_id, user_id)
            )
        return cur.rowcount > 0

    def rename_film(self, user_id: int, film_id: int, title: str) -> str:
        try:
            with self.conn:
                cur = self.conn.execute(
                    "UPDATE films SET title = ?, title_key = ? WHERE id = ? AND user_id = ?",
                    (title, title.casefold(), film_id, user_id),
                )
        except sqlite3.IntegrityError:
            return "exists"
        return "ok" if cur.rowcount else "missing"

    def delete_film(self, user_id: int, film_id: int) -> bool:
        with self.conn:
            cur = self.conn.execute("DELETE FROM films WHERE id = ? AND user_id = ?", (film_id, user_id))
        return cur.rowcount > 0
