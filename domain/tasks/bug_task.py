# domain/tasks/bug_task.py
from .task_base import TaskBase

class BugTask(TaskBase):
    def __init__(self, task_id, title, description, severity):
        super().__init__(task_id, title, description)
        self.severity = severity

    def mark_as_critical(self):
        self.severity = "critical"
