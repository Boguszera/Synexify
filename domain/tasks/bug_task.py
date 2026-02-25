# domain/tasks/bug_task.py

from .task_base import TaskBase


class BugTask(TaskBase):
    VALID_SEVERITIES = {"low", "medium", "high", "critical"}

    def __init__(
        self,
        title: str,
        description: str,
        severity: str,
        task_id: str | None = None,
        project_id: str | None = None,
        sprint_id: str | None = None,
    ):
        super().__init__(
            title=title, description=description, task_id=task_id, project_id=project_id, sprint_id=sprint_id
        )
        if severity not in self.VALID_SEVERITIES:
            raise ValueError(f"Invalid severity '{severity}', must be one of {self.VALID_SEVERITIES}")
        self._severity = severity

    def get_severity(self) -> str:
        return self._severity

    def mark_as_critical(self):
        self._severity = "critical"
