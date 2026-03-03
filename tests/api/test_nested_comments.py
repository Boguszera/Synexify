import uuid

import pytest
from model_bakery import baker

from infrastructure.orm.models.project_model import ProjectModel
from infrastructure.orm.models.task_model import TaskModel


@pytest.mark.django_db
class TestNestedCommentViewSet:
    @pytest.fixture
    def project_with_user(self, manager_user):
        project = baker.make(ProjectModel)
        project.members.add(manager_user)
        return project

    @pytest.fixture
    def task(self, project_with_user):
        return baker.make(TaskModel, project=project_with_user)

    def test_list_comments(self, auth_client, manager_user, task):
        client = auth_client(manager_user)
        response = client.get(f"/api/tasks/{task.id}/comments/")
        assert response.status_code == 200

    def test_create_comment(self, auth_client, manager_user, task):
        client = auth_client(manager_user)
        response = client.post(f"/api/tasks/{task.id}/add_comment/", {"content": "A test comment"})
        assert response.status_code == 201

    def test_nonexistent_task_returns_404(self, auth_client, manager_user):
        client = auth_client(manager_user)
        response = client.get(f"/api/tasks/{uuid.uuid4()}/comments/")
        assert response.status_code == 404

    def test_non_member_returns_403(self, auth_client, other_user, task):
        client = auth_client(other_user)
        response = client.get(f"/api/tasks/{task.id}/comments/")
        assert response.status_code == 403
