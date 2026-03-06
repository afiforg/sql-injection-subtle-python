"""
User routes. Read query params and pass to service. No database or SQL in this file.
"""

from fastapi import APIRouter
from pydantic import BaseModel

from app.state import user_service

router = APIRouter(prefix="/users", tags=["users"])


class UserOut(BaseModel):
    id: int
    username: str
    email: str


@router.get("/search", response_model=dict)
def search(
    q: str | None = None,
    username: str | None = None,
) -> dict:
    # Prefer "q" then "username" so analyzers see multiple taint sources
    term = q or username or ""
    users = user_service.search(term)
    return {"users": [{"id": u.id, "username": u.username, "email": u.email} for u in users]}


@router.get("", response_model=dict)
def list_users(
    sort: str = "id",
    order: str = "asc",
) -> dict:
    users = user_service.list_sorted(sort, order)
    return {"users": [{"id": u.id, "username": u.username, "email": u.email} for u in users]}
