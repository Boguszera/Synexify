# domain/comments/comment.py
from datetime import datetime, timezone
from typing import Any
from domain.users.user_base import UserBase


class Comment:
    def __init__(self, content: str, author: UserBase):
        if not content or not content.strip():
            raise ValueError("Comment content cannot be empty")
        self._content: str = content
        self._author = author
        self._created_at: datetime = datetime.now(timezone.utc)

    def get_content(self) -> str:
        return self._content

    def get_author(self) -> Any:
        return self._author

    def get_created_at(self) -> datetime:
        return self._created_at

    def edit_content(self, new_content: str):
        if not new_content or not new_content.strip():
            raise ValueError("New content cannot be empty")
        self._content = new_content
