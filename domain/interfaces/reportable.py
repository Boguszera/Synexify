# domain/interfaces/reportable.py
from abc import ABC, abstractmethod


class Reportable(ABC):
    @abstractmethod
    def get_report_data(self) -> dict:
        """Return report metrics for further processing in the application."""
        pass
