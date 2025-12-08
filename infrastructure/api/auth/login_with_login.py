# infrastructure/api/auth/login_with_login.py
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from django.contrib.auth import authenticate
from rest_framework.exceptions import AuthenticationFailed

class LoginWithLoginSerializer(TokenObtainPairSerializer):
    def validate(self, attrs):
        login_field = self.username_field
        login = attrs.get(login_field)
        password = attrs.get("password")

        user = authenticate(login=login, password=password)
        if not user:
            raise AuthenticationFailed("Invalid login or password")

        data = super().validate(attrs)
        data["login"] = user.login
        data["role"] = user.role
        return data

class LoginObtainPairView(TokenObtainPairView):
    serializer_class = LoginWithLoginSerializer
