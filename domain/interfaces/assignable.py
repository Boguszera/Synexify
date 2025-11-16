# domain/interfaces/assignable.py
from abc import ABC, abstractmethod

class Assignable(ABC):
    @abstractmethod
    def assign_user(self, user):
        pass

    @abstractmethod
    def get_assignees(self):
        pass