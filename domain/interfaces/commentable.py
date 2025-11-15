# domain/interfaces/commentable.py
from abc import ABC, abstractmethod

class Commentable(ABC):
    @abstractmethod
    def add_comment(self, comment):
        pass