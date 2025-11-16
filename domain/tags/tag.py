# domain/tags/tag.py
from typing import List
from domain.tasks.task_base import TaskBase

class Tag:
    def __init__(self, name: str):
        if not isinstance(name, str) or not name.strip():
            raise ValueError("Tag name must be a non-empty string")
        self._name = name
        self._tasks: List[TaskBase] = []

    def get_name(self) -> str:
        return self._name

    def get_tasks(self) -> List[TaskBase]:
        return list(self._tasks)

    def attach_to_task(self, task: TaskBase):
        if not isinstance(task, TaskBase):
            raise TypeError("task must be a TaskBase instance")
        if task not in self._tasks:
            self._tasks.append(task)
            task.add_tag(self)

    def detach_from_task(self, task: TaskBase):
        if not isinstance(task, TaskBase):
            raise TypeError("task must be a TaskBase instance")
        if task in self._tasks:
            self._tasks.remove(task)
            task.remove_tag(self)
