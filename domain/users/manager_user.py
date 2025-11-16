# domain/users/manager_user.py
from .user_base import UserBase
from domain.tasks.task_base import TaskBase
from domain.users.user_base import UserBase as UserType

class ManagerUser(UserBase):
    def assign_task(self, task, user):
        if not isinstance(task, TaskBase):
            raise TypeError("task must be a TaskBase instance")

        if not isinstance(user, UserType):
            raise TypeError("user must be a UserBase instance")

        task.assign_user(user)

    def create_sprint(self, project):
        from domain.sprints.sprint_base import SprintBase

        if not hasattr(project, "add_sprint") or not callable(project.add_sprint):
            raise TypeError("project must support add_sprint(project) method")

        sprint = SprintBase("New Sprint")
        project.add_sprint(sprint)
        return sprint