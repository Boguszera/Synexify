from django.db import models
from django.db.models.fields import UUIDField, DateTimeField
from typing import TYPE_CHECKING
import uuid

if TYPE_CHECKING:
    from .task_model import TaskModel
    from .user_model import UserModel


class CommentModel(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    task = models.ForeignKey('orm.TaskModel', on_delete=models.CASCADE, related_name='comments')
    author = models.ForeignKey('orm.UserModel', on_delete=models.SET_NULL, null=True)
    task_id: UUIDField[str, str]
    author_id: UUIDField[str, str]

    class Meta:
        db_table = "comments"