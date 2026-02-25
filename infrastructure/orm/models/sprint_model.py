# infrastructure/orm/models/sprint_model.py
import uuid

from django.db import models
from django.utils import timezone


class SprintModel(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=255)
    start_date = models.DateTimeField(default=timezone.now)
    end_date = models.DateTimeField(default=timezone.now)
    project = models.ForeignKey("orm.ProjectModel", on_delete=models.CASCADE, related_name="sprints")

    class Meta:
        db_table = "sprints"

    def __str__(self):
        return self.name
