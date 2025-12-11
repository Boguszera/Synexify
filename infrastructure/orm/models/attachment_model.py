from django.db import models
from django.db.models.fields import UUIDField, DateTimeField
from typing import TYPE_CHECKING
import uuid

if TYPE_CHECKING:
    from .task_model import TaskModel
    from .user_model import UserModel

class AttachmentModel(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    filename = models.CharField(max_length=500)
    uploaded_at = models.DateTimeField(auto_now_add=True)
    task = models.ForeignKey('orm.TaskModel', on_delete=models.CASCADE, related_name='attachments', null=True, blank=True)
    uploaded_by = models.ForeignKey('orm.UserModel', on_delete=models.SET_NULL, null=True)

    # Type Hinting
    task_id: UUIDField[str, str]
    uploaded_by_id: UUIDField[str, str]

    class Meta:
        db_table = "attachments"