# infrastructure/orm/models/user_model.py
from django.db import models
import uuid

class UserModel(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=200)
    email = models.EmailField(unique=True)
    role = models.CharField(max_length=50)
    login = models.CharField(max_length=150, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "users"