# infrastructure/orm/models/sprint_model.py
from django.db import models
from django.utils import timezone
from infrastructure.orm.models.project_model import ProjectModel
import uuid

class SprintModel(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=255)
    start_date = models.DateTimeField(default=timezone.now)
    end_date = models.DateTimeField(default=timezone.now)
    project = models.ForeignKey('orm.ProjectModel', on_delete=models.CASCADE, related_name="sprints")

    class Meta:
        db_table = "sprints"