from abc import ABC, abstractmethod
from typing import Optional, List
from domain.tasks.task_base import TaskBase

class TaskRepository(ABC):
    @abstractmethod
    def get_by_id(self, task_id: str) -> Optional[TaskBase]:
        pass

    @abstractmethod
    def save(self, task: TaskBase) -> None:
        pass

    @abstractmethod
    def delete(self, task_id: str) -> None:
        pass

    @abstractmethod
    def list_by_project(self, project_id: str) -> List[TaskBase]:
        pass

    @abstractmethod
    def list_by_sprint(self, sprint_id: str) -> List[TaskBase]:
        pass
