"""App state: DB connection and services. Initialized at startup."""

import sqlite3
from pathlib import Path

from app.database.schema import init_schema
from app.repositories.user_repository import UserRepository
from app.services.user_service import UserService

db_conn: sqlite3.Connection | None = None
user_service: UserService | None = None


def init(db_path: Path) -> None:
    global db_conn, user_service
    db_conn = sqlite3.connect(db_path)
    db_conn.row_factory = sqlite3.Row
    init_schema(db_conn)
    user_service = UserService(UserRepository(db_conn))
