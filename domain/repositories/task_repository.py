from abc import ABC, abstractmethod

from domain.tasks.task_base import TaskBase


class TaskRepository(ABC):
    @abstractmethod
    def get_by_id(self, task_id: str) -> TaskBase | None:
        pass

    @abstractmethod
    def save(self, task: TaskBase) -> None:
        pass

    @abstractmethod
    def delete(self, task_id: str) -> None:
        pass

    @abstractmethod
    def list_by_project(self, project_id: str) -> list[TaskBase]:
        pass

    @abstractmethod
    def list_by_sprint(self, sprint_id: str) -> list[TaskBase]:
        pass

    @abstractmethod
    def get_all(self) -> list[TaskBase]:
        pass
