import pytest


@pytest.mark.django_db
class TestAuth:
    def test_login_valid_credentials(self, api_client, admin_user):
        response = api_client.post(
            "/api/auth/login/",
            {"login": "admin_user", "password": "adminpass123"},
        )
        assert response.status_code == 200
        assert "access" in response.data
        assert "refresh" in response.data
        assert "login" in response.data
        assert "role" in response.data

    def test_login_invalid_credentials(self, api_client):
        response = api_client.post(
            "/api/auth/login/",
            {"login": "nonexistent", "password": "wrongpass"},
        )
        assert response.status_code == 401

    def test_refresh_valid_token(self, api_client, admin_user):
        login_response = api_client.post(
            "/api/auth/login/",
            {"login": "admin_user", "password": "adminpass123"},
        )
        refresh_token = login_response.data["refresh"]

        response = api_client.post("/api/auth/refresh/", {"refresh": refresh_token})
        assert response.status_code == 200
        assert "access" in response.data

    def test_refresh_invalid_token(self, api_client):
        response = api_client.post("/api/auth/refresh/", {"refresh": "invalidtoken"})
        assert response.status_code == 401

    def test_unauthenticated_request_returns_401(self, api_client):
        response = api_client.get("/api/projects/")
        assert response.status_code == 401
