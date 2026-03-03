import uuid

import pytest
from django.core.files.uploadedfile import SimpleUploadedFile
from model_bakery import baker

from infrastructure.orm.models.project_model import ProjectModel
from infrastructure.orm.models.task_model import TaskModel


@pytest.mark.django_db
class TestTaskViewSet:
    @pytest.fixture
    def project_with_manager(self, manager_user):
        project = baker.make(ProjectModel)
        project.members.add(manager_user)
        return project

    @pytest.fixture
    def task(self, project_with_manager):
        return baker.make(TaskModel, project=project_with_manager, title="Test Task")

    def test_list_tasks(self, auth_client, manager_user):
        client = auth_client(manager_user)
        response = client.get("/api/tasks/")
        assert response.status_code == 200

    def test_list_tasks_with_status_filter(self, auth_client, manager_user, task):
        client = auth_client(manager_user)
        response = client.get("/api/tasks/?status=todo")
        assert response.status_code == 200

    def test_create_task(self, auth_client, manager_user, project_with_manager):
        client = auth_client(manager_user)
        data = {
            "project_id": str(project_with_manager.id),
            "title": "New Task",
            "description": "Task description",
            "type": "feature",
        }
        response = client.post("/api/tasks/", data)
        assert response.status_code == 201

    def test_retrieve_task(self, auth_client, manager_user, task):
        client = auth_client(manager_user)
        response = client.get(f"/api/tasks/{task.id}/")
        assert response.status_code == 200

    def test_retrieve_nonexistent_task_returns_404(self, auth_client, manager_user):
        client = auth_client(manager_user)
        response = client.get(f"/api/tasks/{uuid.uuid4()}/")
        assert response.status_code == 404

    def test_update_task(self, auth_client, manager_user, task):
        client = auth_client(manager_user)
        response = client.put(f"/api/tasks/{task.id}/", {"title": "Updated Title"})
        assert response.status_code == 200

    def test_delete_task(self, auth_client, manager_user, task):
        client = auth_client(manager_user)
        response = client.delete(f"/api/tasks/{task.id}/")
        assert response.status_code == 204

    def test_assign_task_with_assignee_id(self, auth_client, manager_user, team_member_user, task):
        client = auth_client(manager_user)
        response = client.patch(f"/api/tasks/{task.id}/assign/", {"assignee_id": str(team_member_user.id)})
        assert response.status_code == 200

    def test_assign_task_without_assignee_id_returns_400(self, auth_client, manager_user, task):
        client = auth_client(manager_user)
        response = client.patch(f"/api/tasks/{task.id}/assign/", {})
        assert response.status_code == 400

    def test_add_comment(self, auth_client, manager_user, task):
        client = auth_client(manager_user)
        response = client.post(f"/api/tasks/{task.id}/add_comment/", {"content": "A comment"})
        assert response.status_code == 201

    def test_list_comments(self, auth_client, manager_user, task):
        client = auth_client(manager_user)
        response = client.get(f"/api/tasks/{task.id}/comments/")
        assert response.status_code == 200

    def test_add_attachment(self, auth_client, manager_user, task):
        client = auth_client(manager_user)
        file = SimpleUploadedFile("test.txt", b"file content", content_type="text/plain")
        response = client.post(f"/api/tasks/{task.id}/add_attachment/", {"file": file}, format="multipart")
        assert response.status_code == 201
    def test_list_attachments(self, auth_client, manager_user, task):
        client = auth_client(manager_user)
        response = client.get(f"/api/tasks/{task.id}/attachments/")
        assert response.status_code == 200

    def test_unauthenticated_access_returns_401(self, api_client, task):
        response = api_client.get(f"/api/tasks/{task.id}/")
        assert response.status_code == 401
