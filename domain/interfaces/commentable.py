# domain/interfaces/commentable.py
from abc import ABC, abstractmethod

class Commentable(ABC):
    @abstractmethod
    def add_comment(self, comment_id: str, commenter_id: int | None = None) -> None:
        pass

    @abstractmethod
    def get_comments_ids(self):
        pass