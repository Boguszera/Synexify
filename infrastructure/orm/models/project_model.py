# infrastructure/orm/models/project_model.py
import uuid

from django.db import models


class ProjectModel(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True, default="")
    members = models.ManyToManyField("orm.UserModel", related_name="projects", blank=True)
    archived = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "projects"

    def __str__(self):
        return self.name
