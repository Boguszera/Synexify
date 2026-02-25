from abc import ABC, abstractmethod
from datetime import UTC, datetime


class DomainEvent(ABC):
    def __init__(self):
        self.occurred_at = datetime.now(UTC)

    @abstractmethod
    def get_event_name(self) -> str:
        pass
