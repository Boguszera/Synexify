from abc import ABC, abstractmethod

from domain.comments.comment import Comment


class CommentRepository(ABC):
    @abstractmethod
    def get_by_id(self, comment_id: str) -> Comment | None:
        pass

    @abstractmethod
    def save(self, comment: Comment, task_id: str) -> Comment:
        pass

    @abstractmethod
    def delete(self, comment_id: str) -> None:
        pass

    @abstractmethod
    def list_by_task(self, task_id: str) -> list[Comment]:
        pass
