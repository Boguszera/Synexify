# application/task_service.py
from domain.exceptions.exceptions import PermissionDenied
from domain.tasks.bug_task import BugTask
from domain.tasks.feature_task import FeatureTask
from domain.tasks.chore_task import ChoreTask
import uuid
from domain.comments.comment import Comment
from domain.attachments.attachment import Attachment

class TaskService:
    def __init__(self, auth_service, task_repo, project_repo, notification_service):
        self.auth = auth_service
        self.task_repo = task_repo
        self.project_repo = project_repo
        self.notifications = notification_service

    def create_task(self, project, title, description, task_type, user, severity=None, story_points=None):
        if not self.auth.can_manage_project(user, project):
            raise PermissionDenied("User not allowed to create tasks")

        task_id = str(uuid.uuid4())
        if task_type == "bug":
            task = BugTask(title=title, description=description, severity=severity, task_id=task_id)
        elif task_type == "feature":
            task = FeatureTask(title=title, description=description, story_points=story_points, task_id=task_id)
        elif task_type == "chore":
            task = ChoreTask(title=title, description=description, task_id=task_id)
        else:
            raise ValueError("Invalid task type")
        project.add_task(task)

    def assign_task(self, task, user, assignee):
        if not self.auth.can_assign_task(user, task):
            raise PermissionDenied("User not allowed to assign this task")

        task.assign_user(assignee)
        self.task_repo.save(task)
        self.notifications.notify_task_update(task, event=f"assigned to {assignee.get_name()}")

    def update_status(self, task, user, new_status):
        if not self.auth.can_edit_task(user, task):
            raise PermissionDenied("User not allowed to update this task")

        task.update_status(new_status)
        self.task_repo.save(task)
        self.notifications.notify_task_update(task, event=f"status changed to {new_status}")

    def add_attachment(self, task, user, file):
        if not self.auth.can_view_task(user, task):
            raise PermissionDenied("No permission to add attachment.")

        attachment = Attachment(file.filename, user)
        task.attach_file(attachment)
        self.task_repo.save(task)
        return attachment

    def add_comment(self, task, user, content):
        if not self.auth.can_view_task(user, task):
            raise PermissionDenied("User cannot comment on this task.")

        comment = Comment(content=content, author=user)
        task.add_comment(comment)
        self.task_repo.save(task)
        return comment

    def add_tag(self, task, tag, user):
        if not self.auth.can_manage_project(user, task.project):
            raise PermissionDenied("Not allowed to add tags.")

        task.add_tag(tag)
        self.task_repo.save(task)

    def remove_tag(self, task, tag, user):
        if not self.auth.can_manage_project(user, task.project):
            raise PermissionDenied("Not allowed to remove tags.")

        task.remove_tag(tag)
        self.task_repo.save(task)

    def get_task_filters(self, project=None, user=None, status=None, tag=None, priority=None):
        tasks = self.task_repo.filter(project, user, status, tag, priority)
        return tasks

    def notify_task_update(self, task, event):
        self.notifications.notify(event, task)