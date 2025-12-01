from abc import ABC, abstractmethod
from typing import Optional, List
from domain.sprints.sprint_base import SprintBase

class SprintRepository(ABC):
    @abstractmethod
    def get_by_id(self, sprint_id: int) -> Optional[SprintBase]:
        pass

    @abstractmethod
    def save(self, sprint: SprintBase) -> None:
        pass

    @abstractmethod
    def delete(self, sprint_id: int) -> None:
        pass

    @abstractmethod
    def list_by_project(self, project_id: int) -> List[SprintBase]:
        pass
