import uuid
from datetime import UTC, datetime
from typing import Any


class Comment:
    def __init__(self, content: str, author: Any, comment_id: str | None = None):
        if not content or not content.strip():
            raise ValueError("Comment content cannot be empty")

        self._id = comment_id or str(uuid.uuid4())
        self._content: str = content
        self._author = author

        if author and hasattr(author, "get_id"):
            self._author_id = str(author.get_id())
        else:
            self._author_id = None

        self._created_at: datetime = datetime.now(UTC)

    def get_id(self) -> str:
        return self._id

    def get_content(self) -> str:
        return self._content

    def get_author(self) -> Any:
        return self._author

    def get_author_id(self) -> str | None:
        return self._author_id

    def get_created_at(self) -> datetime:
        return self._created_at

    def edit_content(self, new_content: str):
        if not new_content or not new_content.strip():
            raise ValueError("New content cannot be empty")
        self._content = new_content

    def set_created_at(self, dt: datetime):
        self._created_at = dt
