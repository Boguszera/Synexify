# domain/users/team_member_user.py
from .user_base import UserBase

class TeamMemberUser(UserBase):
    def update_task_status(self, task, status):
        from domain.tasks.task_base import TaskBase

        if not isinstance(task, TaskBase):
            raise TypeError("task must be a TaskBase instance")

        if status not in TaskBase.VALID_STATUSES:
            raise ValueError(f"Invalid status '{status}', must be one of {TaskBase.VALID_STATUSES}")
        task.update_status(status)

    def add_attachment(self, task, file):
        from domain.tasks.task_base import TaskBase
        from domain.attachments.attachment import Attachment

        if not isinstance(task, TaskBase):
            raise TypeError("task must be a TaskBase instance")

        if not file:
            raise ValueError("Attachment file cannot be empty")

        attachment = Attachment(filename=file, uploaded_by=self)
        task.attach_file(attachment)