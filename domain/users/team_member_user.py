# domain/users/team_member_user.py
from .user_base import UserBase

class TeamMemberUser(UserBase):
    def update_task_status(self, task, status):
        task.update_status(status)

    def add_attachment(self, task, file):
        task.attach_file(file)