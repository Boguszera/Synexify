from abc import ABC, abstractmethod
from datetime import datetime, timezone

class DomainEvent(ABC):

    def __init__(self):
        self.occurred_at = datetime.now(timezone.utc)

    @abstractmethod
    def get_event_name(self) -> str:
        pass
