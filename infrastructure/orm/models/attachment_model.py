# infrastructure/orm/models/attachment_model.py
from django.db import models
from infrastructure.orm.models.user_model import UserModel
from infrastructure.orm.models.task_model import TaskModel
import uuid

class AttachmentModel(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    filename = models.CharField(max_length=500)
    uploaded_by = models.ForeignKey(UserModel, on_delete=models.SET_NULL, null=True)
    task = models.ForeignKey(TaskModel, on_delete=models.CASCADE, related_name="attachments", null=True, blank=True)
    uploaded_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "attachments"