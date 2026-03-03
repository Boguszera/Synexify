import pytest
from rest_framework.test import APIClient
from rest_framework_simplejwt.tokens import RefreshToken

from infrastructure.orm.models.user_model import UserModel


@pytest.fixture
def api_client():
    return APIClient()


@pytest.fixture
def admin_user(db):
    return UserModel.objects.create_user(
        login="admin_user",
        email="admin@example.com",
        name="Admin User",
        role="admin",
        password="password123",
    )


@pytest.fixture
def manager_user(db):
    return UserModel.objects.create_user(
        login="manager_user",
        email="manager@example.com",
        name="Manager User",
        role="manager",
        password="password123",
    )


@pytest.fixture
def team_member_user(db):
    return UserModel.objects.create_user(
        login="team_member_user",
        email="team_member@example.com",
        name="Team Member User",
        role="team_member",
        password="password123",
    )


@pytest.fixture
def client_user(db):
    return UserModel.objects.create_user(
        login="client_user",
        email="client@example.com",
        name="Client User",
        role="client",
        password="password123",
    )


@pytest.fixture
def other_user(db):
    return UserModel.objects.create_user(
        login="other_user",
        email="other@example.com",
        name="Other User",
        role="team_member",
        password="password123",
    )


@pytest.fixture
def auth_client():
    def _auth_client(user):
        refresh = RefreshToken.for_user(user)
        access_token = str(refresh.access_token)
        client = APIClient()
        client.credentials(HTTP_AUTHORIZATION=f"Bearer {access_token}")
        return client

    return _auth_client


@pytest.fixture
def auth_header_for():
    def _auth_header(user):
        refresh = RefreshToken.for_user(user)
        access_token = str(refresh.access_token)
        return {"HTTP_AUTHORIZATION": f"Bearer {access_token}"}

    return _auth_header
