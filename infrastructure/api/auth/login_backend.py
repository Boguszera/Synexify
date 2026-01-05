# infrastructure/api/auth/login_backend.py

from django.contrib.auth.backends import ModelBackend
from infrastructure.orm.models.user_model import UserModel


class LoginBackend(ModelBackend):
    def authenticate(self, request, login=None, username=None, password=None, **kwargs):
        user_login = login or username

        if user_login is None or password is None:
            return None

        try:
            user = UserModel.objects.get(login=user_login)
        except UserModel.DoesNotExist:
            return None

        if user.check_password(password) and self.user_can_authenticate(user):
            return user
        return None