# domain/users/manager_user.py
from .user_base import UserBase

class ManagerUser(UserBase):
    def assign_task(self, task, user):
        task.assign_user(user)

    def create_sprint(self, project):
        from domain.sprints.sprint_base import SprintBase
        sprint = SprintBase("New Sprint")
        project.add_sprint(sprint)
        return sprint