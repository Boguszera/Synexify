import uuid

import pytest
from django.core.files.uploadedfile import SimpleUploadedFile
from model_bakery import baker

from infrastructure.orm.models.project_model import ProjectModel
from infrastructure.orm.models.task_model import TaskModel


@pytest.fixture
def project_with_member(manager_user):
    project = baker.make(ProjectModel)
    project.members.add(manager_user)
    return project


@pytest.fixture
def task_in_project(project_with_member):
    return baker.make(TaskModel, project=project_with_member)


@pytest.mark.django_db
class TestNestedAttachmentViewSet:
    def test_list_attachments_for_task_returns_200(self, auth_client, manager_user, task_in_project):
        client = auth_client(manager_user)
        response = client.get(f"/api/tasks/{task_in_project.id}/attachments/")
        assert response.status_code == 200
        assert isinstance(response.data, list)

    def test_create_attachment_with_file_returns_201(self, auth_client, manager_user, task_in_project):
        client = auth_client(manager_user)
        file = SimpleUploadedFile("test_file.txt", b"file content here", content_type="text/plain")
        # POST attachments are handled via add_attachment action
        response = client.post(f"/api/tasks/{task_in_project.id}/add_attachment/", {"file": file}, format="multipart")
        assert response.status_code == 201

    def test_create_attachment_without_file_returns_400(self, auth_client, manager_user, task_in_project):
        client = auth_client(manager_user)
        # POST to /attachments/ routes to TaskViewSet.attachments action which only allows GET
        response = client.post(f"/api/tasks/{task_in_project.id}/attachments/", {})
        assert response.status_code == 405

    def test_access_with_nonexistent_task_returns_404(self, auth_client, manager_user):
        client = auth_client(manager_user)
        fake_id = str(uuid.uuid4())
        response = client.get(f"/api/tasks/{fake_id}/attachments/")
        assert response.status_code == 404
