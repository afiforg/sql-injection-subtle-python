"""
User repository. Builds queries using querybuilder and executes them.
No string concatenation of user input happens in this file—only in querybuilder.
"""

import sqlite3
from typing import List, NamedTuple

from app.querybuilder import build_condition, order_by


class User(NamedTuple):
    id: int
    username: str
    email: str


class UserRepository:
    def __init__(self, conn: sqlite3.Connection) -> None:
        self._conn = conn

    def find_by_username(self, username: str) -> List[User]:
        cond = build_condition("username", username)
        query = f"SELECT id, username, email FROM users WHERE {cond}"
        result = self._conn.execute(query)
        rows = result.fetchall()
        return [User(id=row[0], username=row[1], email=row[2]) for row in rows]

    def find_with_sort(self, sort_column: str, sort_dir: str) -> List[User]:
        order_clause = order_by(sort_column, sort_dir)
        query = f"SELECT id, username, email FROM users {order_clause}"
        result = self._conn.execute(query)
        rows = result.fetchall()
        return [User(id=r[0], username=r[1], email=r[2]) for r in rows]
