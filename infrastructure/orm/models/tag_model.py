# infrastructure/orm/models/tag_model.py
from django.db import models
import uuid

class TagModel(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=100, unique=True)

    class Meta:
        db_table = "tags"