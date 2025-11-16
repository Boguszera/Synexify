from typing import List
from domain.interfaces.reportable import Reportable
from domain.users.user_base import UserBase
from domain.tasks.task_base import TaskBase
from domain.sprints.sprint_base import SprintBase

class ProjectBase(Reportable):
    def __init__(self, project_id: int, name: str, description: str):
        if not isinstance(project_id, int):
            raise TypeError("project_id must be an integer")
        if not isinstance(name, str) or not name.strip():
            raise ValueError("name must be a non-empty string")
        if not isinstance(description, str):
            raise TypeError("description must be a string")

        self._id = project_id
        self._name = name
        self._description = description
        self._members: List[UserBase] = []
        self._tasks: List[TaskBase] = []
        self._sprints: List[SprintBase] = []
        self._archived: bool = False

    def get_id(self) -> int:
        return self._id

    def get_name(self) -> str:
        return self._name

    def get_description(self) -> str:
        return self._description

    def get_members(self) -> List[UserBase]:
        return list(self._members)

    def get_tasks(self) -> List[TaskBase]:
        return list(self._tasks)

    def get_sprints(self) -> List[SprintBase]:
        return list(self._sprints)

    def get_progress(self) -> float:
        if not self._tasks:
            return 0.0
        completed = sum(1 for t in self._tasks if t.get_status() == "done")
        return completed / len(self._tasks) * 100

    def add_member(self, user: UserBase):
        if not isinstance(user, UserBase):
            raise TypeError("User must be a UserBase instance")
        if user in self._members:
            return
        self._members.append(user)

    def remove_member(self, user: UserBase):
        if not isinstance(user, UserBase):
            raise TypeError("Member must be a UserBase instance")
        if user not in self._members:
            raise ValueError("User not a member")
        self._members.remove(user)

    def add_task(self, task: TaskBase):
        if not isinstance(task, TaskBase):
            raise TypeError("Task must be a TaskBase instance")
        if task in self._tasks:
            return
        self._tasks.append(task)

    def add_sprint(self, sprint: SprintBase):
        if not isinstance(sprint, SprintBase):
            raise TypeError("Sprint must be a SprintBase instance")
        if sprint in self._sprints:
            return
        self._sprints.append(sprint)

    def generate_report(self) -> str:
        return f"Project {self._name}: {len(self._tasks)} tasks, {len(self._members)} members"
