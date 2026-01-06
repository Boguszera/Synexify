# domain/sprints/sprint_base.py
from typing import List, Optional, Callable
from domain.interfaces.reportable import Reportable
import uuid

class SprintBase(Reportable):
    def __init__(self, name: str, start_date=None, end_date=None, project_id: Optional[str] = None, sprint_id: Optional[str] = None):
        if not name or not name.strip():
            raise ValueError("Sprint name must be a non-empty string")
        self._id = sprint_id or str(uuid.uuid4())
        self._name = name
        self._task_ids: List[str] = []
        self._start_date = start_date
        self._end_date = end_date
        self._project_id = project_id

    def get_id(self) -> str:
        return self._id

    def get_name(self) -> str:
        return self._name

    def get_task_ids(self) -> List[str]:
        return list(self._task_ids)

    def get_project_id(self) -> Optional[str]:
        return self._project_id

    def get_start_date(self):
        return self._start_date

    def get_end_date(self):
        return self._end_date

    def get_task_count(self) -> int:
        return len(self._task_ids)

    def set_name(self, name: str):
        if not name or not name.strip():
            raise ValueError("Sprint name cannot be empty")
        self._name = name.strip()

    def set_start_date(self, start_date):
        self._start_date = start_date

    def set_end_date(self, end_date):
        self._end_date = end_date

    def add_task_id(self, task_id: str):
        if task_id in self._task_ids:
            return
        self._task_ids.append(task_id)

    def remove_task_id(self, task_id: str):
        if task_id not in self._task_ids:
            raise ValueError("Task not in sprint")
        self._task_ids.remove(task_id)

    def is_empty(self) -> bool:
        return len(self._task_ids) == 0

    def get_report_data(self) -> dict:
        return {
            "sprint_id": self._id,
            "sprint_name": self._name,
            "total_tasks": len(self._task_ids),
            "start_date": self._start_date,
            "end_date": self._end_date,
            "project_id": self._project_id,
        }

 