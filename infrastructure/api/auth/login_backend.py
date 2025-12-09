# infrastructure/api/auth/login_backend.py

from django.contrib.auth.backends import ModelBackend
from infrastructure.orm.models.user_model import UserModel

class LoginBackend(ModelBackend):
    def authenticate(self, request, login=None, password=None, **kwargs):
        if login is None:
            return None
        try:
            user = UserModel.objects.get(login=login)
        except UserModel.DoesNotExist:
            return None
        if user.check_password(password):
            return user
        return None
