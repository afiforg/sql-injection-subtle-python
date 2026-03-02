"""Init schema and seed data. Uses parameterized statements only—no user input."""

import sqlite3


def init_schema(conn: sqlite3.Connection) -> None:
    conn.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT NOT NULL,
            email TEXT NOT NULL
        )
    """)
    conn.execute("""
        INSERT OR IGNORE INTO users (id, username, email) VALUES
        (1, 'admin', 'admin@example.com'),
        (2, 'alice', 'alice@example.com'),
        (3, 'bob', 'bob@example.com')
    """)
    conn.commit()
