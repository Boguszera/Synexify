# domain/projects/project_base.py
from domain.interfaces.reportable import Reportable

class ProjectBase(Reportable):
    def __init__(self, project_id, name, description):
        self._id = project_id
        self._name = name
        self._description = description
        self._members = []
        self._tasks = []
        self._sprints = []

    def add_member(self, user):
        self._members.append(user)

    def remove_member(self, user):
        self._members.remove(user)

    def get_progress(self):
        if not self._tasks:
            return 0
        completed = sum(1 for t in self._tasks if t.status == "done")
        return completed / len(self._tasks) * 100

    def get_task_list(self):
        return self._tasks

    def add_task(self, task):
        self._tasks.append(task)

    def add_sprint(self, sprint):
        self._sprints.append(sprint)

    def generate_report(self):
        return f"Project {self._name}: {len(self._tasks)} tasks, {len(self._members)} members"