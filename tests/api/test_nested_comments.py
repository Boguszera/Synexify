import uuid

import pytest
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
class TestNestedCommentViewSet:
    def test_list_comments_for_task_returns_200(self, auth_client, manager_user, task_in_project):
        client = auth_client(manager_user)
        response = client.get(f"/api/tasks/{task_in_project.id}/comments/")
        assert response.status_code == 200
        assert isinstance(response.data, list)

    def test_create_comment_returns_201(self, auth_client, manager_user, task_in_project):
        client = auth_client(manager_user)
        # POST comments are handled via add_comment action
        response = client.post(f"/api/tasks/{task_in_project.id}/add_comment/", {"content": "Test comment"})
        assert response.status_code == 201

    def test_access_with_nonexistent_task_returns_404(self, auth_client, manager_user):
        client = auth_client(manager_user)
        fake_id = str(uuid.uuid4())
        response = client.get(f"/api/tasks/{fake_id}/comments/")
        assert response.status_code == 404

    def test_access_without_project_membership_returns_403(self, auth_client, team_member_user):
        project = baker.make(ProjectModel)  # team_member not a member
        task = baker.make(TaskModel, project=project)
        client = auth_client(team_member_user)
        response = client.get(f"/api/tasks/{task.id}/comments/")
        assert response.status_code == 403
