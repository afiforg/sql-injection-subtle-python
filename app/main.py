"""
FastAPI app. Wiring only—no business logic or SQL.
"""

import sqlite3
from pathlib import Path

from fastapi import FastAPI

from app.database.schema import init_schema
from app.routes import users

# Use a file DB so it persists; same dir as project root
_db_path = Path(__file__).resolve().parent.parent / "data.db"


def create_app() -> FastAPI:
    app = FastAPI(title="Subtle SQL Injection API (Python)")
    app.include_router(users.router)

    @app.on_event("startup")
    def startup() -> None:
        conn = sqlite3.connect(_db_path)
        conn.row_factory = sqlite3.Row
        init_schema(conn)
        app.state.db_conn = conn

    @app.get("/")
    def root() -> dict:
        return {
            "message": "Subtle SQL injection API (Python)",
            "endpoints": [
                "GET /users/search?q= or ?username=",
                "GET /users?sort=&order=",
            ],
        }

    return app


app = create_app()
