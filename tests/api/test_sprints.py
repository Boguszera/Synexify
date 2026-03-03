import uuid
from datetime import timedelta

import pytest
from django.utils import timezone
from model_bakery import baker

from infrastructure.orm.models.project_model import ProjectModel
from infrastructure.orm.models.sprint_model import SprintModel
from infrastructure.orm.models.task_model import TaskModel


@pytest.fixture
def project_with_manager(manager_user):
    project = baker.make(ProjectModel)
    project.members.add(manager_user)
    return project


@pytest.fixture
def sprint_in_project(project_with_manager):
    now = timezone.now()
    return baker.make(SprintModel, project=project_with_manager, start_date=now, end_date=now + timedelta(days=14))


@pytest.mark.django_db
class TestSprintViewSetList:
    def test_list_sprints_returns_200(self, auth_client, manager_user):
        client = auth_client(manager_user)
        response = client.get("/api/sprints/")
        assert response.status_code == 200
        assert isinstance(response.data, list)


@pytest.mark.django_db
class TestSprintViewSetCreate:
    def test_create_sprint_as_manager_member_returns_201(self, auth_client, manager_user, project_with_manager):
        client = auth_client(manager_user)
        now = timezone.now()
        data = {
            "project_id": str(project_with_manager.id),
            "name": "Sprint 1",
            "start_date": now.isoformat(),
            "end_date": (now + timedelta(days=14)).isoformat(),
        }
        response = client.post("/api/sprints/", data)
        assert response.status_code == 201
        assert response.data["project_id"] == str(project_with_manager.id)

    def test_create_sprint_non_member_returns_403(self, auth_client, manager_user):
        project = baker.make(ProjectModel)  # manager not a member
        client = auth_client(manager_user)
        now = timezone.now()
        data = {
            "project_id": str(project.id),
            "name": "Sprint",
            "start_date": now.isoformat(),
            "end_date": (now + timedelta(days=7)).isoformat(),
        }
        response = client.post("/api/sprints/", data)
        assert response.status_code == 403

    def test_create_sprint_unauthenticated_returns_401(self, api_client, project_with_manager):
        now = timezone.now()
        data = {
            "project_id": str(project_with_manager.id),
            "name": "Sprint",
            "start_date": now.isoformat(),
            "end_date": (now + timedelta(days=7)).isoformat(),
        }
        response = api_client.post("/api/sprints/", data)
        assert response.status_code == 401


@pytest.mark.django_db
class TestSprintViewSetRetrieve:
    def test_get_sprint_returns_200(self, auth_client, manager_user, sprint_in_project):
        client = auth_client(manager_user)
        response = client.get(f"/api/sprints/{sprint_in_project.id}/")
        assert response.status_code == 200

    def test_get_nonexistent_sprint_returns_404(self, auth_client, manager_user):
        client = auth_client(manager_user)
        fake_id = str(uuid.uuid4())
        response = client.get(f"/api/sprints/{fake_id}/")
        assert response.status_code == 404


@pytest.mark.django_db
class TestSprintViewSetUpdate:
    def test_patch_sprint_returns_200(self, auth_client, manager_user, sprint_in_project):
        client = auth_client(manager_user)
        response = client.put(f"/api/sprints/{sprint_in_project.id}/", {"name": "Updated Sprint"})
        assert response.status_code == 200


@pytest.mark.django_db
class TestSprintViewSetDelete:
    def test_delete_sprint_returns_204(self, auth_client, manager_user, sprint_in_project):
        client = auth_client(manager_user)
        response = client.delete(f"/api/sprints/{sprint_in_project.id}/")
        assert response.status_code == 204

    def test_delete_nonexistent_sprint_returns_404(self, auth_client, manager_user):
        client = auth_client(manager_user)
        fake_id = str(uuid.uuid4())
        response = client.delete(f"/api/sprints/{fake_id}/")
        assert response.status_code == 404


@pytest.mark.django_db
class TestSprintAddTask:
    def test_add_task_to_sprint_returns_200(self, auth_client, manager_user, project_with_manager, sprint_in_project):
        task = baker.make(TaskModel, project=project_with_manager)
        client = auth_client(manager_user)
        response = client.post(f"/api/sprints/{sprint_in_project.id}/add_task/", {"task_id": str(task.id)})
        assert response.status_code == 200

    def test_add_task_without_task_id_returns_400(self, auth_client, manager_user, sprint_in_project):
        client = auth_client(manager_user)
        response = client.post(f"/api/sprints/{sprint_in_project.id}/add_task/", {})
        assert response.status_code == 400


@pytest.mark.django_db
class TestSprintTasks:
    def test_get_sprint_tasks_returns_200(self, auth_client, manager_user, sprint_in_project):
        client = auth_client(manager_user)
        response = client.get(f"/api/sprints/{sprint_in_project.id}/tasks/")
        assert response.status_code == 200
        assert isinstance(response.data, list)
