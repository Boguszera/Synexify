# infrastructure/orm/models/comment_model.py
from django.db import models
from infrastructure.orm.models.user_model import UserModel
from infrastructure.orm.models.task_model import TaskModel
import uuid

class CommentModel(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    content = models.TextField()
    task = models.ForeignKey('orm.TaskModel', on_delete=models.CASCADE, related_name='comments')
    author = models.ForeignKey('orm.UserModel', on_delete=models.SET_NULL, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "comments"