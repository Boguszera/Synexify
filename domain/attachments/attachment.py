from datetime import datetime, timezone
from typing import Optional, Any
import uuid


class Attachment:
    def __init__(self, filename: str, uploaded_by: Any, attachment_id: Optional[str] = None):
        if not filename or not filename.strip():
            raise ValueError("Filename cannot be empty")

        self._id = attachment_id or str(uuid.uuid4())
        self._filename: str = filename
        self._uploaded_by = uploaded_by

        if uploaded_by and hasattr(uploaded_by, 'get_id'):
            self._uploaded_by_id = str(uploaded_by.get_id())
        else:
            self._uploaded_by_id = None

        self._uploaded_at = datetime.now(timezone.utc)

    def get_id(self) -> str:
        return self._id

    def get_filename(self) -> str:
        return self._filename

    def get_uploaded_by(self):
        return self._uploaded_by

    def get_uploaded_by_id(self) -> Optional[str]:
        return self._uploaded_by_id

    def get_uploaded_at(self) -> datetime:
        return self._uploaded_at

    def set_uploaded_at(self, dt: datetime):
        self._uploaded_at = dt

    def set_uploaded_by_id(self, user_id: str):
        self._uploaded_by_id = user_id