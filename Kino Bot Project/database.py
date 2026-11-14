import random
import sqlite3

class Database:
    def __init__(self, path: str):
        self.conn = sqlite3.connect(path)
        self.conn.row_factory = sqlite3.Row
        self._create_tables()

    def _create_tables(self)
        with self.conn:
            self.conn.execute(
                """
                CREATE TABLE IF NOT EXISTS films (
                id          INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id     INTEGER NOT NULL,
                title       TEXT    NOT NULL,
                title_key   TEXT    NOT NULL,
                genre       TEXT    NOT NULL,
                hype        INTEGER NOT NULL DEFAULT 0 CHECK (hype BETWEE 0 AND 5),
                watched     INTEGER NOT NULL DEFAULT 0,
                UNIQUE      (user_id, title_key),
                )
                """
            )
    def add_film(self, user_id: int, title: str, genre: str, hype: int) -> int | None:
        try:
            with self.conn:
                cur = self.conn.execute(
                    "INSERT INTO films (user_id, title, title_key, genre, hype) VALUES (?, ?, ?, ?, ?)",
                    (user_id, title, title.casefold(), genre, hype),
                )
        except sqlite3.IntegrityError:
            return None
        return cur.lastrowid

    def get_film(self, user_id, int, film_id: int):
        return self.conn.execute(
            "SELECT * FROM films WHERE id = ? AND user_id = ?", (film_id, user_id,)
        ).fetchone()

    def count_films(self, user_i: int) -> int:
        return self.conn.execute("SELECT COUNT(*) FROM films WHERE user_id = ?", (user_id,)).fetchone()[0]

    def list_films(self, user_id: int, offset: int, limit: int):