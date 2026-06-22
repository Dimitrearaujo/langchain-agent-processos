"""Armazena historico de conversas em SQLite."""

import sqlite3
import os
from datetime import datetime

DB_PATH = os.getenv("DB_PATH", "./data/memory.db")


class ConversationStore:
    def __init__(self):
        self.db = DB_PATH
        self._init()

    def _init(self):
        os.makedirs(os.path.dirname(self.db) if os.path.dirname(self.db) else ".", exist_ok=True)
        conn = sqlite3.connect(self.db)
        conn.execute("""
            CREATE TABLE IF NOT EXISTS conversas (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                input TEXT,
                output TEXT,
                criado_em TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        conn.commit()
        conn.close()

    def save(self, input_text: str, output_text: str):
        conn = sqlite3.connect(self.db)
        conn.execute(
            "INSERT INTO conversas (input, output) VALUES (?, ?)",
            (input_text, output_text)
        )
        conn.commit()
        conn.close()

    def get_recent(self, n: int = 5) -> list:
        conn = sqlite3.connect(self.db)
        rows = conn.execute(
            "SELECT input, output, criado_em FROM conversas ORDER BY id DESC LIMIT ?", (n,)
        ).fetchall()
        conn.close()
        return rows
