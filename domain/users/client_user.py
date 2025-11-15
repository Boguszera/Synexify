# domain/users/client_user.py
from .user_base import UserBase

class ClientUser(UserBase):
    def view_project(self, project):
        return project.get_task_list()