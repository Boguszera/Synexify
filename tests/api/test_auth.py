import pytest
from rest_framework_simplejwt.tokens import RefreshToken


@pytest.mark.django_db()
class TestAuthLogin:
    def test_login_valid_credentials_returns_tokens(self, api_client, admin_user):
        data = {"login": "admin_user", "password": "password123"}
        response = api_client.post("/api/auth/login/", data)
        assert response.status_code == 200
        assert "access" in response.data
        assert "refresh" in response.data
        assert response.data["login"] == "admin_user"
        assert response.data["role"] == "admin"

    def test_login_invalid_credentials_returns_401(self, api_client):
        data = {"login": "nobody", "password": "wrongpassword"}
        response = api_client.post("/api/auth/login/", data)
        assert response.status_code == 401

    def test_login_wrong_password_returns_401(self, api_client, admin_user):
        data = {"login": "admin_user", "password": "wrongpassword"}
        response = api_client.post("/api/auth/login/", data)
        assert response.status_code == 401


@pytest.mark.django_db()
class TestAuthRefresh:
    def test_refresh_valid_token_returns_new_access(self, api_client, admin_user):
        refresh = RefreshToken.for_user(admin_user)
        response = api_client.post("/api/auth/refresh/", {"refresh": str(refresh)})
        assert response.status_code == 200
        assert "access" in response.data

    def test_refresh_invalid_token_returns_401(self, api_client):
        response = api_client.post("/api/auth/refresh/", {"refresh": "invalidtoken"})
        assert response.status_code == 401


@pytest.mark.django_db()
class TestUnauthenticatedAccess:
    def test_unauthenticated_request_to_protected_endpoint_returns_401(self, api_client):
        response = api_client.get("/api/users/")
        assert response.status_code == 401

    def test_unauthenticated_request_to_projects_returns_401(self, api_client):
        response = api_client.get("/api/projects/")
        assert response.status_code == 401

    def test_unauthenticated_request_to_tasks_returns_401(self, api_client):
        response = api_client.get("/api/tasks/")
        assert response.status_code == 401
