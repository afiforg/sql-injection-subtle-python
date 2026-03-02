"""
User service. Forwards arguments to the repository. No SQL or DB here.
"""

from typing import List

from app.repositories.user_repository import User, UserRepository


class UserService:
    def __init__(self, repo: UserRepository) -> None:
        self._repo = repo

    def search(self, username: str) -> List[User]:
        return self._repo.find_by_username(username)

    def list_sorted(self, sort_column: str, sort_dir: str) -> List[User]:
        return self._repo.find_with_sort(sort_column, sort_dir)
