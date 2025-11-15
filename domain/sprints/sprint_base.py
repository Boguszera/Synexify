# domain/sprints/sprint_base.py
from domain.interfaces.reportable import Reportable

class SprintBase(Reportable):
    def __init__(self, name):
        self._name = name
        self._tasks = []

    def add_task(self, task):
        self._tasks.append(task)

    def remove_task(self, task):
        self._tasks.remove(task)

    def get_completion_rate(self):
        if not self._tasks:
            return 0
        completed = sum(1 for t in self._tasks if t.status == "done")
        return completed / len(self._tasks) * 100

    def generate_report(self):
        return f"Sprint {self._name}: {len(self._tasks)} tasks, {self.get_completion_rate():.1f}% complete"