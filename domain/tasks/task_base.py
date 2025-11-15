# domain/tasks/task_base.py
from domain.interfaces.assignable import Assignable
from domain.interfaces.commentable import Commentable

class TaskBase(Assignable, Commentable):
    def __init__(self, task_id, title, description):
        self._id = task_id
        self._title = title
        self._description = description
        self.status = "todo"
        self._assignees = []
        self._comments = []
        self._attachments = []
        self._tags = []

    def assign_user(self, user):
        self._assignees.append(user)

    def update_status(self, status):
        self.status = status

    def add_comment(self, comment):
        self._comments.append(comment)

    def attach_file(self, file):
        self._attachments.append(file)

    def add_tag(self, tag):
        self._tags.append(tag)