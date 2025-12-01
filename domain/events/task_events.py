from domain.events.base_event import DomainEvent
from domain.users.user_base import UserBase
from domain.tasks.task_base import TaskBase

class TaskStatusChangedEvent(DomainEvent):
    def __init__(self, task: TaskBase, old_status: str, new_status: str):
        super().__init__()
        self.task = task
        self.old_status = old_status
        self.new_status = new_status

    def get_event_name(self) -> str:
        return "TaskStatusChanged"


class TaskAssignedEvent(DomainEvent):
    def __init__(self, task: TaskBase, assigned_user: UserBase):
        super().__init__()
        self.task = task
        self.assigned_user = assigned_user

    def get_event_name(self) -> str:
        return "TaskAssigned"


class TaskCommentAddedEvent(DomainEvent):
    def __init__(self, task: TaskBase, commenter: UserBase, comment_content: str):
        super().__init__()
        self.task = task
        self.commenter = commenter
        self.comment_content = comment_content

    def get_event_name(self) -> str:
        return "TaskCommentAdded"


class TaskPriorityUpdatedEvent(DomainEvent):
    def __init__(self, task: TaskBase, old_priority: int, new_priority: int):
        super().__init__()
        self.task = task
        self.old_priority = old_priority
        self.new_priority = new_priority

    def get_event_name(self) -> str:
        return "TaskPriorityUpdated"
