from django.db import models
import uuid

class NotificationModel(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey('orm.UserModel', on_delete=models.CASCADE, related_name='notifications')
    task_id = models.CharField(max_length=255, null=True, blank=True)
    title = models.CharField(max_length=255)
    message = models.TextField()
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "notifications"
        ordering = ['-created_at']