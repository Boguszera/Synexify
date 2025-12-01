# domain/comments/comment.py
from datetime import datetime, timezone
from typing import Any, Optional
from domain.users.user_base import UserBase
import uuid

class Comment:
    def __init__(self, content: str, author: UserBase, comment_id: Optional[str] = None):
        if not content or not content.strip():
            raise ValueError("Comment content cannot be empty")
        self._id = comment_id or str(uuid.uuid4())
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
