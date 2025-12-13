import pytest
from django.utils import timezone
from datetime import timedelta
from model_bakery import baker
from infrastructure.orm.models.project_model import ProjectModel
from infrastructure.orm.models.sprint_model import SprintModel
from infrastructure.orm.models.task_model import TaskModel


@pytest.mark.django_db
class TestSprintAndTaskFlow:

    @pytest.fixture
    def project_env(self, manager_user):
        project = baker.make(ProjectModel)
        project.members.add(manager_user)
        return project

    def test_create_sprint_in_project(self, auth_client, manager_user, project_env):
        client = auth_client(manager_user)
        now = timezone.now()
        data = {
            "name": "Sprint 1",
            "start_date": now,
            "end_date": now + timedelta(days=14),
            "project_id": str(project_env.id)
        }

        response = client.post('/api/sprints/', data)

        assert response.status_code == 201
        assert response.data['project_id'] == str(project_env.id)

    def test_add_task_to_sprint_action(self, auth_client, manager_user, project_env):
        # Arrange
        sprint = baker.make(SprintModel, project=project_env)
        task = baker.make(TaskModel, project=project_env, title="Task 1")

        client = auth_client(manager_user)
        url = f'/api/sprints/{sprint.id}/add_task/'

        # Act
        response = client.post(url, {"task_id": str(task.id)})

        # Assert
        assert response.status_code == 200
        task.refresh_from_db()
        assert task.sprint_id == sprint.id

    def test_add_task_to_sprint_forbidden_for_outsider(self, auth_client, other_user, project_env):
        # Arrange: User nie jest w projekcie
        sprint = baker.make(SprintModel, project=project_env)
        task = baker.make(TaskModel, project=project_env)

        client = auth_client(other_user)
        url = f'/api/sprints/{sprint.id}/add_task/'

        # Act
        response = client.post(url, {"task_id": str(task.id)})

        # Assert
        assert response.status_code == 403 or response.status_code == 404
        # (404 jest możliwe jeśli get_project sprawdza uprawnienia przed zwróceniem obiektu)