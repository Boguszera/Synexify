import pytest
from rest_framework.test import APIClient
from rest_framework_simplejwt.tokens import RefreshToken

from infrastructure.orm.models.project_model import ProjectModel
from infrastructure.orm.models.user_model import UserModel


@pytest.fixture
def api_client():
    return APIClient()


@pytest.fixture
def auth_client():
    def _auth_client(user):
        client = APIClient()
        refresh = RefreshToken.for_user(user)
        client.credentials(HTTP_AUTHORIZATION=f"Bearer {refresh.access_token}")
        return client

    return _auth_client


@pytest.fixture
def auth_header_for():
    def _auth_header_for(user):
        refresh = RefreshToken.for_user(user)
        return {"HTTP_AUTHORIZATION": f"Bearer {refresh.access_token}"}

    return _auth_header_for


@pytest.fixture
@pytest.mark.django_db
def admin_user(db):
    user = UserModel.objects.create_user(
        login="admin_user",
        email="admin@example.com",
        name="Admin User",
        role="admin",
        password="adminpass123",
    )
    user.is_staff = True
    user.save()
    return user


@pytest.fixture
@pytest.mark.django_db
def manager_user(db):
    return UserModel.objects.create_user(
        login="manager_user",
        email="manager@example.com",
        name="Manager User",
        role="manager",
        password="managerpass123",
    )


@pytest.fixture
@pytest.mark.django_db
def team_member_user(db):
    return UserModel.objects.create_user(
        login="team_member_user",
        email="teammember@example.com",
        name="Team Member User",
        role="team_member",
        password="memberpass123",
    )


@pytest.fixture
@pytest.mark.django_db
def client_user(db):
    return UserModel.objects.create_user(
        login="client_user",
        email="client@example.com",
        name="Client User",
        role="client",
        password="clientpass123",
    )


@pytest.fixture
@pytest.mark.django_db
def other_user(db):
    return UserModel.objects.create_user(
        login="other_user",
        email="other@example.com",
        name="Other User",
        role="team_member",
        password="otherpass123",
    )


@pytest.fixture
@pytest.mark.django_db
def project_factory(db):
    def _create_project(user_model, name="Test Project", description="Test Description"):
        from infrastructure.adapters.user_adapter import to_domain_user
        from infrastructure.di import Container

        container = Container()
        domain_user = to_domain_user(user_model)
        project = container.project_service.create_project(name=name, description=description, user=domain_user)
        # Also add user to the project members in ORM for permission checks
        project_orm = ProjectModel.objects.get(id=project.get_id())
        project_orm.members.add(user_model)
        return project

    return _create_project


@pytest.fixture
@pytest.mark.django_db
def task_factory(db):
    def _create_task(user_model, project, title="Test Task", description="", task_type="chore"):
        from infrastructure.adapters.user_adapter import to_domain_user
        from infrastructure.di import Container

        container = Container()
        domain_user = to_domain_user(user_model)
        return container.tasks.create_task(
            project=project,
            title=title,
            description=description,
            task_type=task_type,
            user=domain_user,
        )

    return _create_task


@pytest.fixture
@pytest.mark.django_db
def sprint_factory(db):
    def _create_sprint(user_model, project, name="Test Sprint", start_date=None, end_date=None):
        from datetime import timedelta

        from django.utils import timezone

        from infrastructure.adapters.user_adapter import to_domain_user
        from infrastructure.di import Container

        container = Container()
        domain_user = to_domain_user(user_model)
        now = timezone.now()
        return container.sprints.create_sprint(
            project=project,
            name=name,
            start_date=start_date or now,
            end_date=end_date or (now + timedelta(days=14)),
            user=domain_user,
        )

    return _create_sprint
