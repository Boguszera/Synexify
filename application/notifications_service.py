from domain.events.task_events import (
    TaskStatusChangedEvent,
    TaskAssignedEvent,
    TaskCommentAddedEvent,
    TaskPriorityUpdatedEvent,
)
from domain.users.user_base import UserBase
from domain.tasks.task_base import TaskBase
from domain.events.base_event import DomainEvent

class NotificationsService:
    def __init__(self, notification_sender):
        """
        notification_sender: abstraction responsible for sending notifications
        """
        self.notification_sender = notification_sender

    def notify(self, event: DomainEvent):
        """
        General method to notify users based on the domain event.
        Dispatches to specific handlers depending on event type.
        """
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

    # ---- Handlers for specific events ----
    def _notify_task_status_changed(self, event: TaskStatusChangedEvent):
        for user in event.task.get_assignees():
            self._send_notification(user, event.task, event.get_event_name(),
                                    extra_data={"old_status": event.old_status, "new_status": event.new_status})

    def _notify_task_assigned(self, event: TaskAssignedEvent):
        self._send_notification(event.assigned_user, event.task, event.get_event_name())

    def _notify_task_comment_added(self, event: TaskCommentAddedEvent):
        for user in event.task.get_assignees():
            if user != event.commenter:
                self._send_notification(
                    user,
                    event.task,
                    event.get_event_name(),
                    extra_data={"comment": event.comment_content, "commenter_id": event.commenter.get_id()}
                )

    def _notify_task_priority_updated(self, event: TaskPriorityUpdatedEvent):
        for user in event.task.get_assignees():
            self._send_notification(
                user,
                event.task,
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
        self.notification_sender.send(payload)
