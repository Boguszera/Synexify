# infrastructure/orm/models/attachment_model.py

from django.db import models
from typing import TYPE_CHECKING
import uuid
from django.utils import timezone

if TYPE_CHECKING:
    from django.db.models.fields import UUIDField
    from .task_model import TaskModel
    from .user_model import UserModel

class AttachmentModel(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    filename = models.CharField(max_length=500)
    uploaded_at = models.DateTimeField(default=timezone.now)

    task = models.ForeignKey('orm.TaskModel', on_delete=models.CASCADE, related_name='attachments', null=True, blank=True)
    uploaded_by = models.ForeignKey('orm.UserModel', on_delete=models.SET_NULL, null=True)

    # --- POPRAWKA: Ukrywamy to przed Runtime ---
    if TYPE_CHECKING:
        task_id: UUIDField
        uploaded_by_id: UUIDField

    class Meta:
        db_table = "attachments"