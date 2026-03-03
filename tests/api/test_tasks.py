import uuid

import pytest
from django.core.files.uploadedfile import SimpleUploadedFile
from model_bakery import baker

from infrastructure.orm.models.project_model import ProjectModel
from infrastructure.orm.models.task_model import TaskModel


@pytest.fixture()
def project_with_member(manager_user):
    project = baker.make(ProjectModel)
    project.members.add(manager_user)
    return project


@pytest.fixture()
def task_in_project(project_with_member):
    return baker.make(TaskModel, project=project_with_member)


@pytest.mark.django_db()
class TestTaskViewSetList:
    def test_list_tasks_returns_200(self, auth_client, manager_user):
        client = auth_client(manager_user)
        response = client.get("/api/tasks/")
        assert response.status_code == 200
        assert isinstance(response.data, list)

    def test_list_tasks_with_status_filter_returns_200(self, auth_client, manager_user, project_with_member):
        baker.make(TaskModel, project=project_with_member, status="todo")
        client = auth_client(manager_user)
        response = client.get("/api/tasks/?status=todo")
        assert response.status_code == 200

    def test_list_tasks_unauthenticated_returns_401(self, api_client):
        response = api_client.get("/api/tasks/")
        assert response.status_code == 401


@pytest.mark.django_db()
class TestTaskViewSetCreate:
    def test_create_task_returns_201(self, auth_client, manager_user, project_with_member):
        client = auth_client(manager_user)
        data = {
            "project_id": str(project_with_member.id),
            "title": "New Task",
            "description": "Task description",
            "type": "feature",
        }
        response = client.post("/api/tasks/", data)
        assert response.status_code == 201
        assert response.data["title"] == "New Task"

    def test_create_task_unauthenticated_returns_401(self, api_client, project_with_member):
        data = {"project_id": str(project_with_member.id), "title": "Task"}
        response = api_client.post("/api/tasks/", data)
        assert response.status_code == 401


@pytest.mark.django_db()
class TestTaskViewSetRetrieve:
    def test_get_task_returns_200(self, auth_client, manager_user, task_in_project):
        client = auth_client(manager_user)
        response = client.get(f"/api/tasks/{task_in_project.id}/")
        assert response.status_code == 200

    def test_get_nonexistent_task_returns_404(self, auth_client, manager_user):
        client = auth_client(manager_user)
        fake_id = str(uuid.uuid4())
        response = client.get(f"/api/tasks/{fake_id}/")
        assert response.status_code == 404


@pytest.mark.django_db()
class TestTaskViewSetUpdate:
    def test_patch_task_returns_200(self, auth_client, manager_user, task_in_project):
        client = auth_client(manager_user)
        response = client.patch(f"/api/tasks/{task_in_project.id}/", {"title": "Updated Title"})
        assert response.status_code == 200


@pytest.mark.django_db()
class TestTaskViewSetDelete:
    def test_delete_task_returns_204(self, auth_client, manager_user, task_in_project):
        client = auth_client(manager_user)
        response = client.delete(f"/api/tasks/{task_in_project.id}/")
        assert response.status_code == 204


@pytest.mark.django_db()
class TestTaskAssign:
    def test_assign_task_with_assignee_id_returns_200(
        self, auth_client, manager_user, team_member_user, task_in_project
    ):
        client = auth_client(manager_user)
        response = client.patch(
            f"/api/tasks/{task_in_project.id}/assign/",
            {"assignee_id": str(team_member_user.id)},
        )
        assert response.status_code == 200

    def test_assign_task_without_assignee_id_returns_400(self, auth_client, manager_user, task_in_project):
        client = auth_client(manager_user)
        response = client.patch(f"/api/tasks/{task_in_project.id}/assign/", {})
        assert response.status_code == 400


@pytest.mark.django_db()
class TestTaskCommentActions:
    def test_add_comment_returns_201(self, auth_client, manager_user, task_in_project):
        client = auth_client(manager_user)
        response = client.post(f"/api/tasks/{task_in_project.id}/add_comment/", {"content": "A comment"})
        assert response.status_code == 201

    def test_get_comments_returns_200(self, auth_client, manager_user, task_in_project):
        client = auth_client(manager_user)
        response = client.get(f"/api/tasks/{task_in_project.id}/comments/")
        assert response.status_code == 200


@pytest.mark.django_db()
class TestTaskAttachmentActions:
    def test_add_attachment_returns_201(self, auth_client, manager_user, task_in_project):
        client = auth_client(manager_user)
        file = SimpleUploadedFile("test.txt", b"file content", content_type="text/plain")
        response = client.post(
            f"/api/tasks/{task_in_project.id}/add_attachment/",
            {"file": file},
            format="multipart",
        )
        assert response.status_code == 201
        assert response.data["filename"] == "test.txt"

    def test_get_attachments_returns_200(self, auth_client, manager_user, task_in_project):
        client = auth_client(manager_user)
        response = client.get(f"/api/tasks/{task_in_project.id}/attachments/")
        assert response.status_code == 200
