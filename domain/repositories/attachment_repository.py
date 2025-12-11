from abc import ABC, abstractmethod
from domain.attachments.attachment import Attachment
from typing import Optional, List


class AttachmentRepository(ABC):
    @abstractmethod
    def get_by_id(self, attachment_id: str) -> Optional[Attachment]:
        pass

    @abstractmethod
    def save(self, attachment: Attachment, task_id: str, file_data=None) -> Attachment:
        pass

    @abstractmethod
    def delete(self, attachment_id: str) -> None:
        pass

    @abstractmethod
    def list_by_task(self, task_id: str) -> List[Attachment]:
        pass

    @abstractmethod
    def count_by_task(self, task_id: str) -> int:
        pass

    @abstractmethod
    def exists_by_filename(self, filename: str, task_id: str) -> bool:
        pass

    @abstractmethod
    def get_file_content(self, attachment_id: str) -> bytes:
        pass