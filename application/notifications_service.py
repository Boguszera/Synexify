from domain.events.task_events import (
    TaskStatusChangedEvent,
    TaskAssignedEvent,
    TaskCommentAddedEvent,
    TaskPriorityUpdatedEvent,
)
from domain.users.user_base import UserBase
from domain.tasks.task_base import TaskBase
from domain.events.base_events import DomainEvent

class NotificationsService:
    def __init__(self, task_repo, user_repo):
        self.task_repo = task_repo
        self.user_repo = user_repo
        self.notifications: list[dict] = []

    def notify(self, event: DomainEvent):
        if isinstance(event, TaskStatusChangedEvent):
            self._notify_task_status_changed(event)
        elif isinstance(event, TaskAssignedEvent):
            self._notify_task_assigned(event)
        elif isinstance(event, TaskCommentAddedEvent):
            self._notify_task_comment_added(event)
        elif isinstance(event, TaskPriorityUpdatedEvent):
            self._notify_task_priority_updated(event)
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

    def _send_notification(self, user: UserBase, task: TaskBase, event_name: str, extra_data: dict = None):
        payload = {
            "user_id": user.get_id(),
            "task_id": task.get_id(),
            "event": event_name,
        }
        if extra_data:
            payload.update(extra_data)
        self.notifications.append(payload)
        print(f"[NOTIFICATION] {payload}")