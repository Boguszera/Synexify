import pytest


@pytest.mark.django_db
class TestReportingEndpoints:
    def test_dashboard_returns_200(self, auth_client, admin_user):
        client = auth_client(admin_user)
        response = client.get("/api/reporting/dashboard/")
        assert response.status_code == 200
        assert "message" in response.data

    def test_dashboard_unauthenticated_returns_401(self, api_client):
        response = api_client.get("/api/reporting/dashboard/")
        assert response.status_code == 401
