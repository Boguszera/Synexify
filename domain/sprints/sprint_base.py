# domain/sprints/sprint_base.py
from typing import List
from domain.interfaces.reportable import Reportable
from domain.tasks.task_base import TaskBase

class SprintBase(Reportable):
    def __init__(self, name: str):
        if not isinstance(name, str) or not name.strip():
            raise ValueError("Sprint name must be a non-empty string")
        self._name = name
        self._tasks: List[TaskBase] = []

    def get_name(self) -> str:
        return self._name

    def get_tasks(self) -> List[TaskBase]:
        return list(self._tasks)

    def get_completion_rate(self) -> float:
        if not self._tasks:
            return 0.0
        completed = sum(1 for t in self._tasks if t.get_status() == "done")
        return completed / len(self._tasks) * 100

    def add_task(self, task: TaskBase):
        if not isinstance(task, TaskBase):
            raise TypeError("task must be a TaskBase instance")
        if task in self._tasks:
            return
        self._tasks.append(task)

    def remove_task(self, task: TaskBase):
        if not isinstance(task, TaskBase):
            raise TypeError("task must be a TaskBase instance")
        if task not in self._tasks:
            raise ValueError("Task not in sprint")
        self._tasks.remove(task)

    def generate_report(self) -> str:
        return f"Sprint {self._name}: {len(self._tasks)} tasks, {self.get_completion_rate():.1f}% complete"
