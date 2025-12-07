# infrastructure/di.py
# dependency injection
from application.admin_panel_service import AdminPanelService
from application.backlog_service import BacklogService
from application.notifications_service import NotificationsService
from application.reporting_service import ReportingService
from application.sprint_service import SprintService
from application.task_service import TaskService
from application.authorization_service import AuthorizationService

from infrastructure.repositories.user_django_repository import UserDjangoRepository
from infrastructure.repositories.project_django_repository import ProjectDjangoRepository
from infrastructure.repositories.task_django_repository import TaskDjangoRepository
from infrastructure.repositories.sprint_django_repository import SprintDjangoRepository

class Container:
    def __init__(self):
        # --- REPOSITORIES ---
        self.user_repo = UserDjangoRepository()
        self.project_repo = ProjectDjangoRepository()
        self.task_repo = TaskDjangoRepository()
        self.sprint_repo = SprintDjangoRepository()

        # --- SERVICES (domain / external) ---
        self.auth = AuthorizationService()

        # --- APPLICATION SERVICES ---
        self.admin_panel = AdminPanelService(
            auth_service=self.auth,
            user_repo=self.user_repo,
            project_repo=self.project_repo,
        )

        self.backlog = BacklogService(
            auth_service=self.auth,
            task_repo=self.task_repo,
        )

        self.notifications = NotificationsService(
            task_repo=self.task_repo,
            user_repo=self.user_repo,
        )

        self.reporting = ReportingService(
            auth_service=self.auth,
            task_repo=self.task_repo,
        )

        self.sprints = SprintService(
            auth_service=self.auth,
            sprint_repo=self.sprint_repo,
            project_repo=self.project_repo,
        )

        self.tasks = TaskService(
            auth_service=self.auth,
            task_repo=self.task_repo,
            project_repo=self.project_repo,
            notification_service=self.notifications,
        )
