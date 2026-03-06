"""
FastAPI app. Wiring only—no business logic or SQL.
"""

from pathlib import Path

from fastapi import FastAPI

from app.routes import users
from app.state import init as init_state

# Use a file DB so it persists; same dir as project root
_db_path = Path(__file__).resolve().parent.parent / "data.db"


def create_app() -> FastAPI:
    app = FastAPI(title="Subtle SQL Injection API (Python)")
    app.include_router(users.router)

    @app.on_event("startup")
    def startup() -> None:
        init_state(_db_path)

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
