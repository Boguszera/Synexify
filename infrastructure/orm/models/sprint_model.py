# infrastructure/orm/models/sprint_model.py
from django.db import models
from infrastructure.orm.models.project_model import ProjectModel
# import uuid

class SprintModel(models.Model):
    id = models.AutoField(primary_key=True)  # integer PK
    name = models.CharField(max_length=255)
    project = models.ForeignKey(ProjectModel, on_delete=models.CASCADE, related_name="sprints")
    start_date = models.DateTimeField(null=True, blank=True)
    end_date = models.DateTimeField(null=True, blank=True)

    class Meta:
        db_table = "sprints"