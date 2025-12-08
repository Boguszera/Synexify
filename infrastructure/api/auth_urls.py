from django.urls import path
from infrastructure.api.auth.login_with_login import LoginObtainPairView
from rest_framework_simplejwt.views import TokenRefreshView

urlpatterns = [
    path("login/", LoginObtainPairView.as_view(), name="token_obtain_pair"),
    path("refresh/", TokenRefreshView.as_view(), name="token_refresh"),
]