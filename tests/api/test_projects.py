import uuid

import pytest
from model_bakery import baker

from infrastructure.orm.models.project_model import ProjectModel


@pytest.mark.django_db
class TestProjectViewSet:
    @pytest.fixture
    def project_with_manager(self, manager_user):
        project = baker.make(ProjectModel, name="Manager Project")
        project.members.add(manager_user)
        return project

    def test_list_projects_as_authenticated_user(self, auth_client, admin_user):
        client = auth_client(admin_user)
        response = client.get("/api/projects/")
        assert response.status_code == 200

    def test_create_project_as_manager(self, auth_client, manager_user):
        client = auth_client(manager_user)
        response = client.post("/api/projects/", {"name": "New Project", "description": "Desc"})
        assert response.status_code == 201
        assert response.data["name"] == "New Project"

    def test_create_project_as_team_member_returns_403(self, auth_client, team_member_user):
        client = auth_client(team_member_user)
        response = client.post("/api/projects/", {"name": "New Project"})
        assert response.status_code == 403

    def test_retrieve_project_as_member(self, auth_client, manager_user, project_with_manager):
        client = auth_client(manager_user)
        response = client.get(f"/api/projects/{project_with_manager.id}/")
        assert response.status_code == 200
        assert response.data["name"] == "Manager Project"

    def test_retrieve_project_as_non_member_returns_403(self, auth_client, other_user, project_with_manager):
        client = auth_client(other_user)
        response = client.get(f"/api/projects/{project_with_manager.id}/")
        assert response.status_code == 403

    def test_retrieve_nonexistent_project_returns_404(self, auth_client, admin_user):
        client = auth_client(admin_user)
        response = client.get(f"/api/projects/{uuid.uuid4()}/")
        assert response.status_code == 404

    def test_update_project_as_manager(self, auth_client, manager_user, project_with_manager):
        client = auth_client(manager_user)
        response = client.put(f"/api/projects/{project_with_manager.id}/", {"name": "Updated Name"})
        assert response.status_code == 200

    def test_update_project_as_non_member_returns_403(self, auth_client, other_user, project_with_manager):
        client = auth_client(other_user)
        response = client.put(f"/api/projects/{project_with_manager.id}/", {"name": "Should Fail"})
        assert response.status_code in (403, 404)

    def test_delete_project_as_manager(self, auth_client, manager_user, project_with_manager):
        client = auth_client(manager_user)
        response = client.delete(f"/api/projects/{project_with_manager.id}/")
        assert response.status_code == 204

    def test_delete_nonexistent_project_returns_404(self, auth_client, admin_user):
        client = auth_client(admin_user)
        response = client.delete(f"/api/projects/{uuid.uuid4()}/")
        assert response.status_code == 404
