# infrastructure/orm/models/comment_model.py

from django.db import models
from typing import TYPE_CHECKING
import uuid

if TYPE_CHECKING:
    from django.db.models.fields import UUIDField
    from .task_model import TaskModel
    from .user_model import UserModel

class CommentModel(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    # Relacje (to one tworzą pola _id w bazie)
    task = models.ForeignKey('orm.TaskModel', on_delete=models.CASCADE, related_name='comments')
    author = models.ForeignKey('orm.UserModel', on_delete=models.SET_NULL, null=True)

    # --- POPRAWKA: Ukrywamy to przed Pythonem w czasie działania (Runtime) ---
    if TYPE_CHECKING:
        # To widzi tylko Twój IDE (PyCharm/VS Code) i Linter
        task_id: UUIDField
        author_id: UUIDField

    class Meta:
        db_table = "comments"