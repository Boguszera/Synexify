# domain/interfaces/assignable.py
from abc import ABC, abstractmethod
from typing import List

class Assignable(ABC):
    @abstractmethod
    def assign_user_id(self, user_id: int) -> None:
        pass

    @abstractmethod
    def get_assignees_ids(self) -> List[int]:
        pass