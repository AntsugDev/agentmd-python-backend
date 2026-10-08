"""Database initialization and management."""

import sqlite3
from pathlib import Path
from typing import Optional

from agentmd.config import settings


class Database:
    _instance: Optional["Database"] = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._initialized = False
        return cls._instance

    def __init__(self):
        if self._initialized:
            return

        self.db_path = Path(settings.database_path)
        self.db_path.parent.mkdir(parents=True, exist_ok=True)
        self.conn: Optional[sqlite3.Connection] = None
        self._connect()
        self._create_tables()
        self._initialized = True

    def _connect(self) -> None:
        self.conn = sqlite3.connect(
            str(self.db_path),
            check_same_thread=False,
            detect_types=sqlite3.PARSE_DECLTYPES,
        )
        self.conn.row_factory = sqlite3.Row
        self.conn.execute("PRAGMA journal_mode=WAL")
        self.conn.execute("PRAGMA synchronous=NORMAL")

    def _create_tables(self) -> None:
        if not self.conn:
            return

        cursor = self.conn.cursor()

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS STATUS (
                ID INTEGER PRIMARY KEY AUTOINCREMENT,
                NAME TEXT UNIQUE NOT NULL
            )
        """)

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS LOCK (
                KEY TEXT PRIMARY KEY,
                VALUE INTEGER DEFAULT 0
            )
        """)

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS FILES (
                ID INTEGER PRIMARY KEY AUTOINCREMENT,
                FILE_NAME TEXT NOT NULL,
                CONTENT TEXT,
                TAG TEXT,
                STATUS_ID INTEGER,
                MODEL_USED TEXT,
                MIME_TYPE TEXT,
                EXT TEXT,
                CREATED_AT TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                UPDATED_AT TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS CHUNKS (
                ID INTEGER PRIMARY KEY AUTOINCREMENT,
                FILE_ID INTEGER,
                CHUNK_INDEX INTEGER,
                CONTENT TEXT NOT NULL,
                EMBEDDING BLOB,
                CREATED_AT TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS WORKED_LOG (
                ID INTEGER PRIMARY KEY AUTOINCREMENT,
                LEVEL TEXT,
                MESSAGE TEXT,
                CONTEXT TEXT,
                CREATED_AT TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS DATALIST (
                ID INTEGER PRIMARY KEY AUTOINCREMENT,
                NAME TEXT,
                DESCRIPTION TEXT,
                VALUE TEXT
            )
        """)

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS DATALIST_AMM (
                ID INTEGER PRIMARY KEY AUTOINCREMENT,
                NAME TEXT,
                DESCRIPTION TEXT,
                VALUE TEXT
            )
        """)

        self.conn.commit()

    def get_connection(self) -> sqlite3.Connection:
        if not self.conn:
            self._connect()
        return self.conn

    def execute(self, query: str, params: tuple = ()):
        if not self.conn:
            raise RuntimeError("Database not connected")
        return self.conn.execute(query, params)

    def commit(self) -> None:
        if self.conn:
            self.conn.commit()

    def rollback(self) -> None:
        if self.conn:
            self.conn.rollback()

    def close(self) -> None:
        if self.conn:
            self.conn.close()
            self.conn = None


# Global singleton

db = Database()
