from abc import ABC, abstractmethod
from typing import Optional, List
from domain.projects.project_base import ProjectBase

class ProjectRepository(ABC):
    @abstractmethod
    def get_by_id(self, project_id: int) -> Optional[ProjectBase]:
        pass

    @abstractmethod
    def save(self, project: ProjectBase) -> None:
        pass

    @abstractmethod
    def delete(self, project_id: int) -> None:
        pass

    @abstractmethod
    def list_all(self) -> List[ProjectBase]:
        pass
