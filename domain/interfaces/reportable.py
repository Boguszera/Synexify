# domain/interfaces/reportable.py
from abc import ABC, abstractmethod

class Reportable(ABC):
    @abstractmethod
    def generate_report(self):
        pass