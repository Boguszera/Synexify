# domain/tasks/task_base.py
from domain.interfaces.assignable import Assignable
from domain.interfaces.commentable import Commentable
from domain.events.task_events import TaskStatusChangedEvent, TaskAssignedEvent, TaskCommentAddedEvent
from typing import List, Optional
import uuid

class InvalidStatusError(Exception):
    pass

class TaskBase(Assignable, Commentable):

    VALID_STATUSES = {"todo", "in_progress", "done", "blocked"}

    def __init__(self, task_id: Optional[str], title: str, description: str, project_id: str = None, sprint_id: Optional[str] = None):
        self._id = task_id or str(uuid.uuid4())
        self._title = title
        self._description = description
        self._status = "todo"
        self._assignee_ids: List[str] = []
        self._comment_ids: List[str] = []
        self._attachment_ids: List[str] = []
        self._tag_ids: List[str] = []
        self._project_id = project_id
        self._sprint_id = sprint_id
        self._domain_events = []

    def get_id(self) -> str:
        return self._id

    def get_title(self) -> str:
        return self._title

    def get_description(self) -> str:
        return self._description

    def get_status(self) -> str:
        return self._status

    def get_assignee_ids(self) -> List[str]:
        return list(self._assignee_ids)

    def get_comments_ids(self) -> List[str]:
        return list(self._comment_ids)

    def get_attachment_ids(self) -> List[str]:
        return list(self._attachment_ids)

    def get_tag_ids(self) -> List[str]:
        return list(self._tag_ids)

    def get_project_id(self) -> Optional[str]:
        return self._project_id

    def get_sprint_id(self) -> Optional[str]:
        return self._sprint_id

    def get_assignees_ids(self) -> List[str]:
        return list(self._assignee_ids)

    # behavior
    def assign_user_id(self, user_id: str):
        if user_id in self._assignee_ids:
            return
        self._assignee_ids.append(user_id)
        # raise domain event
        self._domain_events.append(TaskAssignedEvent(task_id=self._id, assigned_user_id=user_id))

    def update_status(self, new_status: str):
        if new_status not in self.VALID_STATUSES:
            raise InvalidStatusError(f'Invalid status "{new_status}"')
        old = self._status
        if old == new_status:
            return
        self._status = new_status
        self._domain_events.append(TaskStatusChangedEvent(task_id=self._id, old_status=old, new_status=new_status))

    def add_comment(self, comment_id: str, commenter_id: Optional[str] = None) -> None:
        if comment_id in self._comment_ids:
            return
        self._comment_ids.append(comment_id)
        self._domain_events.append(
            TaskCommentAddedEvent(task_id=self._id, commenter_id=commenter_id, comment_id=comment_id))

    def attach_file_id(self, attachment_id: str):
        if attachment_id in self._attachment_ids:
            return
        self._attachment_ids.append(attachment_id)

    def add_tag_id(self, tag_id: str):
        if tag_id in self._tag_ids:
            return
        self._tag_ids.append(tag_id)

    def remove_tag_id(self, tag_id: str):
        if tag_id in self._tag_ids:
            self._tag_ids.remove(tag_id)

    def set_sprint_id(self, sprint_id: str):
        self._sprint_id = sprint_id

    # domain events accessor
    def pull_domain_events(self):
        events = list(self._domain_events)
        self._domain_events.clear()
        return events