import uuid
from datetime import timedelta

import pytest
from django.utils import timezone
from model_bakery import baker

from infrastructure.orm.models.project_model import ProjectModel
from infrastructure.orm.models.sprint_model import SprintModel
from infrastructure.orm.models.task_model import TaskModel


@pytest.mark.django_db
class TestSprintViewSet:
    @pytest.fixture
    def project_with_manager(self, manager_user):
        project = baker.make(ProjectModel)
        project.members.add(manager_user)
        return project

    @pytest.fixture
    def sprint(self, project_with_manager):
        now = timezone.now()
        return baker.make(SprintModel, project=project_with_manager, name="Sprint 1", start_date=now, end_date=now + timedelta(days=14))

    def test_list_sprints(self, auth_client, manager_user):
        client = auth_client(manager_user)
        response = client.get("/api/sprints/")
        assert response.status_code == 200

    def test_create_sprint(self, auth_client, manager_user, project_with_manager):
        client = auth_client(manager_user)
        now = timezone.now()
        data = {
            "project_id": str(project_with_manager.id),
            "name": "New Sprint",
            "start_date": now,
            "end_date": now + timedelta(days=14),
        }
        response = client.post("/api/sprints/", data)
        assert response.status_code == 201
        assert response.data["project_id"] == str(project_with_manager.id)

    def test_create_sprint_as_non_member_returns_403(self, auth_client, other_user, project_with_manager):
        client = auth_client(other_user)
        now = timezone.now()
        data = {
            "project_id": str(project_with_manager.id),
            "name": "Sprint X",
            "start_date": now,
            "end_date": now + timedelta(days=14),
        }
        response = client.post("/api/sprints/", data)
        assert response.status_code == 403

    def test_retrieve_sprint(self, auth_client, manager_user, sprint):
        client = auth_client(manager_user)
        response = client.get(f"/api/sprints/{sprint.id}/")
        assert response.status_code == 200

    def test_retrieve_nonexistent_sprint_returns_404(self, auth_client, manager_user):
        client = auth_client(manager_user)
        response = client.get(f"/api/sprints/{uuid.uuid4()}/")
        assert response.status_code == 404

    def test_update_sprint(self, auth_client, manager_user, sprint):
        client = auth_client(manager_user)
        response = client.put(f"/api/sprints/{sprint.id}/", {"name": "Updated Sprint"})
        assert response.status_code == 200

    def test_delete_sprint(self, auth_client, manager_user, sprint):
        client = auth_client(manager_user)
        response = client.delete(f"/api/sprints/{sprint.id}/")
        assert response.status_code == 204

    def test_delete_nonexistent_sprint_returns_404(self, auth_client, manager_user):
        client = auth_client(manager_user)
        response = client.delete(f"/api/sprints/{uuid.uuid4()}/")
        assert response.status_code == 404

    def test_add_task_to_sprint(self, auth_client, manager_user, project_with_manager, sprint):
        task = baker.make(TaskModel, project=project_with_manager)
        client = auth_client(manager_user)
        response = client.post(f"/api/sprints/{sprint.id}/add_task/", {"task_id": str(task.id)})
        assert response.status_code == 200

    def test_add_task_without_task_id_returns_400(self, auth_client, manager_user, sprint):
        client = auth_client(manager_user)
        response = client.post(f"/api/sprints/{sprint.id}/add_task/", {})
        assert response.status_code == 400

    def test_list_sprint_tasks(self, auth_client, manager_user, sprint):
        client = auth_client(manager_user)
        response = client.get(f"/api/sprints/{sprint.id}/tasks/")
        assert response.status_code == 200
