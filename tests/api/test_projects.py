import uuid

import pytest
from model_bakery import baker

from infrastructure.orm.models.project_model import ProjectModel


@pytest.mark.django_db
class TestProjectViewSetList:
    def test_list_projects_as_authenticated_user_returns_200(self, auth_client, admin_user):
        client = auth_client(admin_user)
        response = client.get("/api/projects/")
        assert response.status_code == 200
        assert isinstance(response.data, list)

    def test_list_projects_returns_only_visible_projects_for_member(self, auth_client, manager_user):
        project = baker.make(ProjectModel)
        project.members.add(manager_user)
        baker.make(ProjectModel)  # not a member
        client = auth_client(manager_user)
        response = client.get("/api/projects/")
        assert response.status_code == 200
        ids = [str(p["id"]) for p in response.data]
        assert str(project.id) in ids


@pytest.mark.django_db
class TestProjectViewSetCreate:
    def test_create_project_as_manager_returns_201(self, auth_client, manager_user):
        client = auth_client(manager_user)
        data = {"name": "New Project", "description": "A test project"}
        response = client.post("/api/projects/", data)
        assert response.status_code == 201
        assert response.data["name"] == "New Project"

    def test_create_project_as_team_member_returns_403(self, auth_client, team_member_user):
        client = auth_client(team_member_user)
        data = {"name": "Forbidden Project", "description": "Should fail"}
        response = client.post("/api/projects/", data)
        assert response.status_code == 403

    def test_create_project_as_admin_returns_201(self, auth_client, admin_user):
        client = auth_client(admin_user)
        data = {"name": "Admin Project", "description": "Created by admin"}
        response = client.post("/api/projects/", data)
        assert response.status_code == 201


@pytest.mark.django_db
class TestProjectViewSetRetrieve:
    def test_get_project_as_member_returns_200(self, auth_client, manager_user):
        project = baker.make(ProjectModel)
        project.members.add(manager_user)
        client = auth_client(manager_user)
        response = client.get(f"/api/projects/{project.id}/")
        assert response.status_code == 200
        assert str(response.data["id"]) == str(project.id)

    def test_get_project_as_non_member_returns_403(self, auth_client, team_member_user):
        project = baker.make(ProjectModel)
        client = auth_client(team_member_user)
        response = client.get(f"/api/projects/{project.id}/")
        assert response.status_code == 403

    def test_get_nonexistent_project_returns_404(self, auth_client, admin_user):
        client = auth_client(admin_user)
        fake_id = str(uuid.uuid4())
        response = client.get(f"/api/projects/{fake_id}/")
        assert response.status_code == 404

    def test_get_project_as_admin_returns_200(self, auth_client, admin_user):
        project = baker.make(ProjectModel)
        client = auth_client(admin_user)
        response = client.get(f"/api/projects/{project.id}/")
        assert response.status_code == 200


@pytest.mark.django_db
class TestProjectViewSetUpdate:
    def test_patch_project_as_manager_member_returns_200(self, auth_client, manager_user):
        project = baker.make(ProjectModel)
        project.members.add(manager_user)
        client = auth_client(manager_user)
        response = client.put(f"/api/projects/{project.id}/", {"name": "Updated"})
        assert response.status_code == 200

    def test_patch_project_as_non_member_returns_403(self, auth_client, manager_user):
        project = baker.make(ProjectModel)
        client = auth_client(manager_user)
        response = client.put(f"/api/projects/{project.id}/", {"name": "Should fail"})
        assert response.status_code == 403


@pytest.mark.django_db
class TestProjectViewSetDelete:
    def test_delete_project_as_manager_member_returns_204(self, auth_client, manager_user):
        project = baker.make(ProjectModel)
        project.members.add(manager_user)
        client = auth_client(manager_user)
        response = client.delete(f"/api/projects/{project.id}/")
        assert response.status_code == 204

    def test_delete_nonexistent_project_returns_404(self, auth_client, admin_user):
        client = auth_client(admin_user)
        fake_id = str(uuid.uuid4())
        response = client.delete(f"/api/projects/{fake_id}/")
        assert response.status_code == 404
