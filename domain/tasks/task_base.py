# domain/tasks/task_base.py
from domain.interfaces.assignable import Assignable
from domain.interfaces.commentable import Commentable


class InvalidStatusError(Exception):
    pass

class TaskBase(Assignable, Commentable):

    VALID_STATUSES = {"todo", "in_progress", "done", "blocked"}

    def __init__(self, task_id: int, title: str, description: str):
        self._id = task_id
        self._title = title
        self._description = description
        self._status = "todo"
        self._assignees = []
        self._comments = []
        self._attachments = []
        self._tags = []

    def get_id(self):
        return self._id

    def get_title(self):
        return self._title

    def get_description(self):
        return self._description

    def get_status(self):
        return self._status

    def get_assignees(self):
        return self._assignees

    def get_comments(self):
        return list(self._comments)

    def get_attachments(self):
        return self._attachments

    def get_tags(self):
        return self._tags

    def assign_user(self, user):
        from domain.users.user_base import UserBase
        if not isinstance(user, UserBase):
            raise TypeError("user must be a UserBase instance")
        if user in self._assignees:
            return
        self._assignees.append(user)

    def update_status(self, new_status):
        if new_status not in self.VALID_STATUSES:
            raise InvalidStatusError(f'Invalid status "{new_status}"')
        self._status = new_status

    def add_comment(self, comment):
        from domain.comments.comment import Comment
        if not isinstance(comment, Comment):
            raise TypeError("comment must be a Comment instance")
        self._comments.append(comment)

    def attach_file(self, file):
        from domain.attachments.attachment import Attachment
        if not isinstance(file, Attachment):
            raise TypeError("file must be an Attachment instance")
        self._attachments.append(file)

    def add_tag(self, tag):
        from domain.tags.tag import Tag
        if not isinstance(tag, Tag):
            raise TypeError("tag must be a Tag instance")
        if tag in self._tags:
            return
        self._tags.append(tag)

    def remove_tag(self, tag):
        from domain.tags.tag import Tag
        if not isinstance(tag, Tag):
            raise TypeError("tag must be a Tag instance")
        if tag in self._tags:
            self._tags.remove(tag)