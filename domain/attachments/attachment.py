# domain/attachments/attachment.py
from datetime import datetime, timezone
from domain.users.user_base import UserBase


class Attachment:
    def __init__(self, filename: str, uploaded_by):
        if not filename or not filename.strip():
            raise ValueError("Filename cannot be empty")
        self._filename: str = filename
        self._uploaded_by = uploaded_by
        self._uploaded_at = datetime.now(timezone.utc)

    def get_filename(self) -> str:
        return self._filename

    def get_uploaded_by(self) -> UserBase:
        return self._uploaded_by

    def get_uploaded_at(self) -> datetime:
        return self._uploaded_at

    def download(self):
        pass

    def delete(self):
        pass