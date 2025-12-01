from abc import ABC, abstractmethod
from datetime import datetime

class DomainEvent(ABC):

    def __init__(self):
        self.occurred_at = datetime.utcnow()

    @abstractmethod
    def get_event_name(self) -> str:
        pass
