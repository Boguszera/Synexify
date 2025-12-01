# domain/sprints/sprint_base.py
from typing import List, Dict
from domain.interfaces.reportable import Reportable
from domain.tasks.task_base import TaskBase

class SprintBase(Reportable):
    def __init__(self, name: str, start_date=None, end_date=None, project=None):
        if not isinstance(name, str) or not name.strip():
            raise ValueError("Sprint name must be a non-empty string")
        self._name = name
        self._tasks: List[TaskBase] = []
        self._start_date = start_date
        self._end_date = end_date
        self._project = project

    def get_name(self) -> str:
        return self._name

    def get_tasks(self) -> List[TaskBase]:
        return list(self._tasks)

    def get_completion_rate(self) -> float:
        if not self._tasks:
            return 0.0
        completed = sum(1 for t in self._tasks if t.get_status() == "done")
        return completed / len(self._tasks) * 100

    def get_project(self):
        return self._project

    def set_project(self, project):
        self._project = project

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

    def get_report_data(self) -> Dict:
        total_tasks = len(self.get_tasks())
        done_tasks = len([t for t in self.get_tasks() if t.get_status().lower() == "done"])
        completion = (done_tasks / total_tasks * 100) if total_tasks else 0.0

        return {
            "sprint_name": self.get_name(),
            "total_tasks": total_tasks,
            "tasks_done": done_tasks,
            "completion_percentage": completion
        }