# domain/users/client_user.py
from .user_base import UserBase

class ClientUser(UserBase):
    def view_project(self, project):

        if not hasattr(project, "get_name") or not callable(project.get_name):
            raise TypeError("project must have get_name() method")
        if not hasattr(project, "get_progress") or not callable(project.get_progress):
            raise TypeError("project must have get_progress() method")

        return {
            "project": project.get_name(),
            "progress": project.get_progress()
        }