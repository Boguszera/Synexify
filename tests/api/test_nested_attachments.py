import uuid

import pytest
from django.core.files.uploadedfile import SimpleUploadedFile
from model_bakery import baker

from infrastructure.orm.models.project_model import ProjectModel
from infrastructure.orm.models.task_model import TaskModel


@pytest.mark.django_db
class TestNestedAttachmentViewSet:
    @pytest.fixture
    def project_with_user(self, manager_user):
        project = baker.make(ProjectModel)
        project.members.add(manager_user)
        return project

    @pytest.fixture
    def task(self, project_with_user):
        return baker.make(TaskModel, project=project_with_user)

    def test_list_attachments(self, auth_client, manager_user, task):
        client = auth_client(manager_user)
        response = client.get(f"/api/tasks/{task.id}/attachments/")
        assert response.status_code == 200

    def test_create_attachment_with_file(self, auth_client, manager_user, task):
        client = auth_client(manager_user)
        file = SimpleUploadedFile("test.txt", b"file content", content_type="text/plain")
        response = client.post(f"/api/tasks/{task.id}/add_attachment/", {"file": file}, format="multipart")
        assert response.status_code == 201

    def test_create_attachment_without_file_returns_400(self, auth_client, manager_user, task):
        client = auth_client(manager_user)
        response = client.post(f"/api/tasks/{task.id}/add_attachment/", {})
        assert response.status_code == 400

    def test_nonexistent_task_returns_404(self, auth_client, manager_user):
        client = auth_client(manager_user)
        response = client.get(f"/api/tasks/{uuid.uuid4()}/attachments/")
        assert response.status_code == 404
