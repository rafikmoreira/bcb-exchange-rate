import os
import sqlite3
from datetime import datetime, timezone

from src.domain.entities import LogEntry
from src.domain.ports import LogRepository


class SQLiteLogRepository(LogRepository):
    """Repositório de logs utilizando SQLite como backend de persistência."""

    def __init__(self, db_path: str = "data/db/quotations.db") -> None:
        self.db_path = db_path
        os.makedirs(os.path.dirname(self.db_path), exist_ok=True)
        self._init_db()

    def _init_db(self) -> None:
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS logs (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    level TEXT NOT NULL,
                    message TEXT NOT NULL,
                    context TEXT,
                    created_at TEXT NOT NULL
                )
            """)
            conn.commit()

    def save_log(self, entry: LogEntry) -> None:
        created_at = entry.created_at or datetime.now(timezone.utc).isoformat()
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute(
                "INSERT INTO logs (level, message, context, created_at) VALUES (?, ?, ?, ?)",
                (entry.level, entry.message, entry.context, created_at),
            )
            conn.commit()

    def get_logs(self, level: str | None = None, limit: int = 100) -> list[LogEntry]:
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            if level:
                cursor.execute(
                    "SELECT level, message, context, created_at FROM logs WHERE level = ? ORDER BY id DESC LIMIT ?",
                    (level.upper(), limit),
                )
            else:
                cursor.execute(
                    "SELECT level, message, context, created_at FROM logs ORDER BY id DESC LIMIT ?",
                    (limit,),
                )
            rows = cursor.fetchall()

        return [
            LogEntry(level=row[0], message=row[1], context=row[2], created_at=row[3])
            for row in rows
        ]
