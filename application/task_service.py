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
        self.auth.check_manage_project(user, project)
        task_id = str(uuid.uuid4())
        if task_type == "bug":
            task = BugTask(title=title, description=description, severity=severity, task_id=task_id)
        elif task_type == "feature":
            task = FeatureTask(title=title, description=description, story_points=story_points, task_id=task_id)
        elif task_type == "chore":
            task = ChoreTask(title=title, description=description, task_id=task_id)
        else:
            raise ValueError("Invalid task type")

        project.add_task_id(task.get_id())
        self.task_repo.save(task)
        self.project_repo.save(project)
        return task

    def assign_task(self, task, user, assignee):
        if not self.auth.can_assign_task(user, task):
            raise PermissionDenied(user.get_id(), action="assign_task", resource=f"task:{task.get_id()}")
        task.assign_user_id(assignee.get_id())
        self.task_repo.save(task)

        from domain.events.task_events import TaskAssignedEvent
        event = TaskAssignedEvent(task_id=task.get_id(), assigned_user_id=assignee.get_id())
        self.notifications.notify(event)

    def update_status(self, task, user, new_status):
        if not self.auth.can_edit_task(user, task):
            raise PermissionDenied(user.get_id(), action="update_status", resource=f"task:{task.get_id()}")
        old_status = task.get_status()
        task.update_status(new_status)
        self.task_repo.save(task)

        from domain.events.task_events import TaskStatusChangedEvent
        event = TaskStatusChangedEvent(
            task_id=task.get_id(),
            old_status=old_status,
            new_status=new_status
        )
        self.notifications.notify(event)

    def add_comment(self, task, user, content):
        comment = Comment(content=content, author=user)
        task.add_comment(comment.get_id(), comment.get_author())
        self.task_repo.save(task)

        from domain.events.task_events import TaskCommentAddedEvent
        event = TaskCommentAddedEvent(
            task_id=task.get_id(),
            comment_id=comment.get_id(),
            commenter_id=user.get_id()
        )
        self.notifications.notify(event)
        return comment

    def add_attachment(self, task, user, file):
        attachment = Attachment(filename=file.filename, uploaded_by=user)
        task.attach_file_id(attachment.get_id())
        self.task_repo.save(task)
        return attachment

    def add_tag(self, task, tag):
        task.add_tag_id(tag.get_id())
        self.task_repo.save(task)

    def remove_tag(self, task, tag):
        task.remove_tag_id(tag.get_id())
        self.task_repo.save(task)
