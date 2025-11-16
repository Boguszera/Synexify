# domain/tasks/bug_task.py
from .task_base import TaskBase

class BugTask(TaskBase):

    VALID_SEVERITIES = {"low", "medium", "high", "critical"}

    def __init__(self, task_id: int, title: str, description: str, severity: str):
        super().__init__(task_id, title, description)
        self._set_severity(severity)

    def _set_severity(self, severity: str):
        if severity not in self.VALID_SEVERITIES:
            raise ValueError(f"Invalid severity '{severity}', must be one of {self.VALID_SEVERITIES}")
        self._severity = severity

    def get_severity(self) -> str:
        return self._severity

    def mark_as_critical(self):
        self._severity = "critical"

