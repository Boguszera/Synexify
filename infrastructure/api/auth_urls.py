from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView

from infrastructure.api.auth.login_with_login import LoginObtainPairView

urlpatterns = [
    path("login/", LoginObtainPairView.as_view(), name="token_obtain_pair"),
    path("refresh/", TokenRefreshView.as_view(), name="token_refresh"),
]
