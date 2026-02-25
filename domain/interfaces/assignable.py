# domain/interfaces/assignable.py
from abc import ABC, abstractmethod


class Assignable(ABC):
    @abstractmethod
    def assign_user_id(self, user_id: int) -> None:
        pass

    @abstractmethod
    def get_assignees_ids(self) -> list[int]:
        pass
