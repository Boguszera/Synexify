# infrastructure/orm/models/comment_model.py

import uuid
from typing import TYPE_CHECKING

from django.db import models

if TYPE_CHECKING:
    from django.db.models.fields import UUIDField


class CommentModel(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    task = models.ForeignKey("orm.TaskModel", on_delete=models.CASCADE, related_name="comments")
    author = models.ForeignKey("orm.UserModel", on_delete=models.SET_NULL, null=True)

    if TYPE_CHECKING:
        task_id: UUIDField
        author_id: UUIDField

    class Meta:
        db_table = "comments"

    def __str__(self):
        return self.content
