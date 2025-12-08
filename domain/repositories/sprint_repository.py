from abc import ABC, abstractmethod
from typing import Optional, List
from domain.sprints.sprint_base import SprintBase

class SprintRepository(ABC):
    @abstractmethod
    def get_by_id(self, sprint_id: str) -> Optional[SprintBase]:
        pass

    @abstractmethod
    def save(self, sprint: SprintBase) -> None:
        pass

    @abstractmethod
    def delete(self, sprint_id: str) -> None:
        pass

    @abstractmethod
    def list_by_project(self, project_id: str) -> List[SprintBase]:
        pass
