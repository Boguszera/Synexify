from abc import ABC, abstractmethod

from domain.projects.project_base import ProjectBase


class ProjectRepository(ABC):
    @abstractmethod
    def get_by_id(self, project_id: str) -> ProjectBase | None:
        pass

    @abstractmethod
    def save(self, project: ProjectBase) -> None:
        pass

    @abstractmethod
    def delete(self, project_id: str) -> None:
        pass

    @abstractmethod
    def list_all(self) -> list[ProjectBase]:
        pass
