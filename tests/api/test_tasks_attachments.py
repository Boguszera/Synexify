import pytest
from django.core.files.uploadedfile import SimpleUploadedFile
from model_bakery import baker
from infrastructure.orm.models.task_model import TaskModel
from infrastructure.orm.models.project_model import ProjectModel


@pytest.mark.django_db
class TestTaskAttachments:

    @pytest.fixture
    def setup_task(self, manager_user):
        project = baker.make(ProjectModel)
        project.members.add(manager_user)
        task = baker.make(TaskModel, project=project)
        return task

    def test_upload_attachment_success(self, auth_client, manager_user, setup_task):
        client = auth_client(manager_user)

        # Symulacja pliku
        file_content = b"file_content"
        file = SimpleUploadedFile("test.txt", file_content, content_type="text/plain")

        url = f'/api/tasks/{setup_task.id}/add_attachment/'
        response = client.post(url, {"file": file}, format='multipart')

        assert response.status_code == 201
        assert response.data['filename'] == "test.txt"

    def test_assign_task_permission(self, auth_client, manager_user, team_member_user, setup_task):
        """
        Manager przypisuje zadanie deweloperowi.
        """
        client = auth_client(manager_user)
        url = f'/api/tasks/{setup_task.id}/assign/'

        data = {"assignee_id": str(team_member_user.id)}
        response = client.patch(url, data)

        assert response.status_code == 200
        setup_task.refresh_from_db()
        assert team_member_user in setup_task.assignees.all()