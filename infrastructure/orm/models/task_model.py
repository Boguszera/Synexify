# infrastructure/orm/models/task_model.py
from django.db import models
from infrastructure.orm.models.user_model import UserModel
from infrastructure.orm.models.project_model import ProjectModel
from infrastructure.orm.models.sprint_model import SprintModel
from infrastructure.orm.models.tag_model import TagModel
import uuid

class TaskModel(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    title = models.CharField(max_length=500)
    description = models.TextField(blank=True)
    status = models.CharField(max_length=50, default="todo")

    task_type = models.CharField(max_length=50, default="chore")

    story_points = models.IntegerField(null=True, blank=True)

    severity = models.CharField(
        max_length=20,
        choices=[
            ('low', 'Low'),
            ('medium', 'Medium'),
            ('high', 'High'),
            ('critical', 'Critical'),
        ],
        null=True,
        blank=True
    )
    sprint = models.ForeignKey('orm.SprintModel', on_delete=models.SET_NULL, related_name="tasks", null=True,
                               blank=True)
    project = models.ForeignKey('orm.ProjectModel', on_delete=models.CASCADE, related_name="tasks", null=True,
                                blank=True)
    assignees = models.ManyToManyField('orm.UserModel', related_name="assigned_tasks", blank=True)
    tags = models.ManyToManyField('orm.TagModel', related_name="tasks", blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "tasks"