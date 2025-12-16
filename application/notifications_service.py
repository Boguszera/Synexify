from domain.events.task_events import (
    TaskStatusChangedEvent,
    TaskAssignedEvent,
    TaskCommentAddedEvent,
    TaskPriorityUpdatedEvent,
    TaskUnassignedEvent,
)
from domain.users.user_base import UserBase
from domain.tasks.task_base import TaskBase
from domain.events.base_events import DomainEvent
from infrastructure.orm.models.notification_model import NotificationModel

class NotificationsService:
    def __init__(self, task_repo, user_repo):
        self.task_repo = task_repo
        self.user_repo = user_repo

    def notify(self, event: DomainEvent):
        if isinstance(event, TaskStatusChangedEvent):
            self._notify_task_status_changed(event)
        elif isinstance(event, TaskAssignedEvent):
            self._notify_task_assigned(event)
        elif isinstance(event, TaskCommentAddedEvent):
            self._notify_task_comment_added(event)
        elif isinstance(event, TaskPriorityUpdatedEvent):
            self._notify_task_priority_updated(event)
        elif isinstance(event, TaskUnassignedEvent):
            self._notify_task_unassigned(event)
        else:
            raise ValueError(f"Unsupported event type: {type(event)}")

    def _notify_task_status_changed(self, event: TaskStatusChangedEvent):
        task = self.task_repo.get_by_id(event.task_id)
        for user_id in task.get_assignees_ids():
            user = self.user_repo.get_by_id(user_id)
            self._send_notification(
                user,
                task,
                event.get_event_name(),
                extra_data={"old_status": event.old_status, "new_status": event.new_status}
            )

    def _notify_task_assigned(self, event: TaskAssignedEvent):
        task = self.task_repo.get_by_id(event.task_id)
        user = self.user_repo.get_by_id(event.assigned_user_id)
        self._send_notification(user, task, event.get_event_name())

    def _notify_task_unassigned(self, event: TaskUnassignedEvent):
        task = self.task_repo.get_by_id(event.task_id)
        user = self.user_repo.get_by_id(event.unassigned_user_id)

        if user and task:
            self._send_notification(
                user,
                task,
                event.get_event_name(),
                extra_data={"unassigned_user_id": event.unassigned_user_id}
            )

    def _notify_task_comment_added(self, event: TaskCommentAddedEvent):
        task = self.task_repo.get_by_id(event.task_id)
        commenter = self.user_repo.get_by_id(event.commenter_id)
        for user_id in task.get_assignees_ids():
            if user_id == commenter.get_id():
                continue
            user = self.user_repo.get_by_id(user_id)
            self._send_notification(
                user,
                task,
                event.get_event_name(),
                extra_data={"comment_id": event.comment_id, "commenter_id": commenter.get_id()}
            )

    def _notify_task_priority_updated(self, event: TaskPriorityUpdatedEvent):
        task = self.task_repo.get_by_id(event.task_id)
        for user_id in task.get_assignees_ids():
            user = self.user_repo.get_by_id(user_id)
            self._send_notification(
                user,
                task,
                event.get_event_name(),
                extra_data={"old_priority": event.old_priority, "new_priority": event.new_priority}
            )

    def _send_notification(self, user, task, event_name: str, extra_data: dict = None):
        title = "New event"
        message = f"Event {event_name} in task {task.get_title()}"

        if event_name == "TaskUnassigned":
            title = "Assignment removed"
            message = f"You have been disconnected from the task: {task.get_title()}"
        elif event_name == "TaskAssigned":
            title = "Nowe zadanie"
            message = f"You have been assigned to the task: {task.get_title()}"
        elif event_name == "TaskCommentAdded":
            title = "New comment"
            message = f"Comment added in task: {task.get_title()}"
        NotificationModel.objects.create(
            user_id=user.get_id(),
            task_id=task.get_id(),
            title=title,
            message=message
        )
        print(f"[NOTIFICATION SAVED] User: {user.get_email()} | Msg: {message}")