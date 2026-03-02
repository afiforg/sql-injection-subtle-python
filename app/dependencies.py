"""App-wide dependencies. DB and service are created once per request/context."""

import sqlite3
from pathlib import Path

from fastapi import Request

from app.database.schema import init_schema
from app.repositories.user_repository import UserRepository
from app.services.user_service import UserService

# In-memory DB for demo; path relative to project root
_db_path = Path(__file__).resolve().parent.parent / "data.db"


def get_db_connection() -> sqlite3.Connection:
    conn = sqlite3.connect(_db_path, check_same_thread=False)
    conn.row_factory = sqlite3.Row
    return conn


def _ensure_schema(conn: sqlite3.Connection) -> None:
    init_schema(conn)


def get_user_service(request: Request) -> UserService:
    # Use app-state connection so schema is inited once
    conn = request.app.state.db_conn
    repo = UserRepository(conn)
    return UserService(repo)
