# domain/events/task_events.py
from domain.events.base_events import DomainEvent

class TaskStatusChangedEvent(DomainEvent):
    def __init__(self, task_id: str, old_status: str, new_status: str):
        super().__init__()
        self.task_id = task_id
        self.old_status = old_status
        self.new_status = new_status

    def get_event_name(self) -> str:
        return "TaskStatusChanged"


class TaskAssignedEvent(DomainEvent):
    def __init__(self, task_id: str, assigned_user_id: str):
        super().__init__()
        self.task_id = task_id
        self.assigned_user_id = assigned_user_id

    def get_event_name(self) -> str:
        return "TaskAssigned"


class TaskCommentAddedEvent(DomainEvent):
    def __init__(self, task_id: str, commenter_id: str | None, comment_id: str):
        super().__init__()
        self.task_id = task_id
        self.commenter_id = commenter_id
        self.comment_id = comment_id

    def get_event_name(self) -> str:
        return "TaskCommentAdded"


class TaskPriorityUpdatedEvent(DomainEvent):
    def __init__(self, task_id: str, old_priority: int, new_priority: int):
        super().__init__()
        self.task_id = task_id
        self.old_priority = old_priority
        self.new_priority = new_priority

    def get_event_name(self) -> str:
        return "TaskPriorityUpdated"
