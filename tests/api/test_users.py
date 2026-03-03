import uuid

import pytest

from infrastructure.orm.models.user_model import UserModel


@pytest.mark.django_db
class TestUserViewSetList:
    def test_list_users_as_admin_returns_200(self, auth_client, admin_user):
        client = auth_client(admin_user)
        response = client.get("/api/users/")
        assert response.status_code == 200

    def test_list_users_as_non_admin_returns_403(self, auth_client, manager_user):
        client = auth_client(manager_user)
        response = client.get("/api/users/")
        assert response.status_code == 403

    def test_list_users_as_team_member_returns_403(self, auth_client, team_member_user):
        client = auth_client(team_member_user)
        response = client.get("/api/users/")
        assert response.status_code == 403


@pytest.mark.django_db
class TestUserViewSetCreate:
    def test_create_user_as_admin_returns_201(self, auth_client, admin_user):
        client = auth_client(admin_user)
        data = {
            "name": "New User",
            "email": "newuser@example.com",
            "role": "team_member",
            "login": "newuser",
            "password": "securepass123",
        }
        response = client.post("/api/users/", data)
        assert response.status_code == 201
        assert response.data["login"] == "newuser"

    def test_create_user_as_non_admin_returns_403(self, auth_client, manager_user):
        client = auth_client(manager_user)
        data = {
            "name": "New User",
            "email": "newuser2@example.com",
            "role": "team_member",
            "login": "newuser2",
            "password": "securepass123",
        }
        response = client.post("/api/users/", data)
        assert response.status_code == 403


@pytest.mark.django_db
class TestUserViewSetRetrieve:
    def test_get_user_as_admin_returns_200(self, auth_client, admin_user, manager_user):
        client = auth_client(admin_user)
        response = client.get(f"/api/users/{manager_user.id}/")
        assert response.status_code == 200
        assert response.data["login"] == "manager_user"

    def test_get_nonexistent_user_returns_404(self, auth_client, admin_user):
        client = auth_client(admin_user)
        fake_id = str(uuid.uuid4())
        response = client.get(f"/api/users/{fake_id}/")
        assert response.status_code == 404

    def test_get_user_as_non_admin_returns_403(self, auth_client, manager_user, team_member_user):
        client = auth_client(manager_user)
        response = client.get(f"/api/users/{team_member_user.id}/")
        assert response.status_code == 403


@pytest.mark.django_db
class TestUserViewSetUpdate:
    def test_update_user_as_admin_returns_200(self, auth_client, admin_user, manager_user):
        client = auth_client(admin_user)
        data = {"name": "Updated Name"}
        response = client.put(f"/api/users/{manager_user.id}/", data)
        assert response.status_code == 200

    def test_update_user_as_non_admin_returns_403(self, auth_client, manager_user, team_member_user):
        client = auth_client(manager_user)
        data = {"name": "Updated Name"}
        response = client.put(f"/api/users/{team_member_user.id}/", data)
        assert response.status_code == 403


@pytest.mark.django_db
class TestUserViewSetDelete:
    def test_delete_user_as_admin_returns_204(self, auth_client, admin_user):
        target = UserModel.objects.create_user(
            login="todelete",
            email="todelete@example.com",
            name="To Delete",
            role="team_member",
            password="password123",
        )
        client = auth_client(admin_user)
        response = client.delete(f"/api/users/{target.id}/")
        assert response.status_code == 204

    def test_delete_nonexistent_user_returns_404(self, auth_client, admin_user):
        client = auth_client(admin_user)
        fake_id = str(uuid.uuid4())
        response = client.delete(f"/api/users/{fake_id}/")
        assert response.status_code == 404

    def test_delete_user_as_non_admin_returns_403(self, auth_client, manager_user, team_member_user):
        client = auth_client(manager_user)
        response = client.delete(f"/api/users/{team_member_user.id}/")
        assert response.status_code == 403
