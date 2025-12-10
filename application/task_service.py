# application/task_service.py
from domain.exceptions.exceptions import PermissionDenied
from domain.tasks.bug_task import BugTask
from domain.tasks.feature_task import FeatureTask
from domain.tasks.chore_task import ChoreTask
import uuid
from domain.comments.comment import Comment
from domain.attachments.attachment import Attachment

class TaskService:
    def __init__(self, auth_service, task_repo, project_repo, notification_service, user_repo):
        self.auth = auth_service
        self.task_repo = task_repo
        self.project_repo = project_repo
        self.notifications = notification_service
        self.user_repo = user_repo

    def create_task(self, project, title, description, task_type, user, severity=None, story_points=None):
        self.auth.check_manage_project(user, project)
        task_id = str(uuid.uuid4())
        project_id = project.get_id()
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

    def assign_task(self, task, user, assignee_id: str):
        assignee = self.user_repo.get_by_id(assignee_id)
        if assignee is None:
            raise ValueError(f"Assignee user ID {assignee_id} not found.")
        if not self.auth.can_assign_task(user, task):
            if user.get_id() != assignee.get_id():
                raise PermissionDenied(user.get_id(), action="assign_task_other", resource=f"task:{task.get_id()}")
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

    def get_task_filters(self, project=None, user=None, status=None, tag=None, priority=None):
        tasks = self.task_repo.get_all()

        if project:
            tasks = [t for t in tasks if t.get_project_id() == project.get_id()]
        if user:
            tasks = [t for t in tasks if user.get_id() in t.get_assignees_ids()]
        if status:
            tasks = [t for t in tasks if t.get_status() == status]
        if tag:
            tasks = [t for t in tasks if any(tid == tag.get_id() for tid in t.get_tag_ids())]
        return tasks

    def update_task(self, task, user, **fields):
        project_id = task.get_project_id()
        project = self.project_repo.get_by_id(project_id)
        if project is None:
            raise PermissionDenied(user.get_id(), action="update_task", resource=f"project:{project_id or 'None'}")
        self.auth.check_manage_project(user, project)

        allowed_fields = {"title", "description"}

        for key, value in fields.items():
            if key in allowed_fields:
                setattr(task, f"_{key}", value)
            elif key == "status":
                self.update_status(task, user, value)
            # dodać obsługę innych pól (np. severity, story_points, assignee_id)

        return self.task_repo.save(task)

    def delete_task(self, task_id: str, user):
        task = self.task_repo.get_by_id(task_id)
        if not task:
            return
        project = self.project_repo.get_by_id(task.get_project_id())
        self.auth.check_manage_project(user, project)

        # 3. Usuń Task z Projektu (nie wiem, trzeba zobaczyc implementacje ProjectBase)
        # project.remove_task_id(task.get_id())
        # self.project_repo.save(project)

        self.task_repo.delete(task_id)
