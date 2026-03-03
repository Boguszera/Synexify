import pytest


@pytest.mark.django_db
class TestUserViewSet:
    def test_list_users_as_admin(self, auth_client, admin_user):
        client = auth_client(admin_user)
        response = client.get("/api/users/")
        assert response.status_code == 200

    def test_list_users_as_non_admin(self, auth_client, manager_user):
        client = auth_client(manager_user)
        response = client.get("/api/users/")
        assert response.status_code == 403

    def test_create_user_as_admin(self, auth_client, admin_user):
        client = auth_client(admin_user)
        data = {
            "name": "New User",
            "email": "newuser@example.com",
            "role": "team_member",
            "login": "newlogin",
            "password": "newpass123",
        }
        response = client.post("/api/users/", data)
        assert response.status_code == 201
        assert response.data["login"] == "newlogin"

    def test_retrieve_user_as_admin(self, auth_client, admin_user, manager_user):
        client = auth_client(admin_user)
        response = client.get(f"/api/users/{manager_user.id}/")
        assert response.status_code == 200
        assert response.data["login"] == "manager_user"

    def test_retrieve_nonexistent_user(self, auth_client, admin_user):
        import uuid

        client = auth_client(admin_user)
        response = client.get(f"/api/users/{uuid.uuid4()}/")
        assert response.status_code == 404

    def test_update_user_as_admin(self, auth_client, admin_user, team_member_user):
        client = auth_client(admin_user)
        response = client.put(f"/api/users/{team_member_user.id}/", {"name": "Updated Name"})
        assert response.status_code == 200

    def test_delete_user_as_admin(self, auth_client, admin_user, team_member_user):
        client = auth_client(admin_user)
        response = client.delete(f"/api/users/{team_member_user.id}/")
        assert response.status_code == 204

    def test_delete_nonexistent_user(self, auth_client, admin_user):
        import uuid

        client = auth_client(admin_user)
        response = client.delete(f"/api/users/{uuid.uuid4()}/")
        assert response.status_code == 404

    def test_crud_as_non_admin_returns_403(self, auth_client, team_member_user):
        client = auth_client(team_member_user)
        assert client.get("/api/users/").status_code == 403
        assert client.post("/api/users/", {}).status_code == 403
