# appcore/management/commands/seed.py

from django.core.management.base import BaseCommand
from infrastructure.repositories.user_django_repository import UserDjangoRepository
from infrastructure.repositories.project_django_repository import ProjectDjangoRepository
from infrastructure.repositories.task_django_repository import TaskDjangoRepository
from infrastructure.repositories.sprint_django_repository import SprintDjangoRepository

from domain.users.admin_user import AdminUser
from domain.users.manager_user import ManagerUser
from domain.users.team_member_user import TeamMemberUser
from domain.users.client_user import ClientUser

from domain.projects.project_base import ProjectBase
from domain.sprints.sprint_base import SprintBase
from domain.tasks.bug_task import BugTask

import uuid
from datetime import datetime, timedelta


class Command(BaseCommand):
    help = "Seed database"

    def handle(self, *args, **options):

        print("Seeding users...")

        user_repo = UserDjangoRepository()
        project_repo = ProjectDjangoRepository()
        sprint_repo = SprintDjangoRepository()
        task_repo = TaskDjangoRepository()

        users = {}
        role_map = [
            ("admin", "root"),
            ("manager", "mgr1"),
            ("team_member", "member1"),
            ("client", "client1")
        ]

        for role, login in role_map:
            existing = user_repo.get_by_login(login)
            if existing:
                print(f"User {login} exists")
                users[role] = existing
                continue

            domain_cls = {
                "admin": AdminUser,
                "manager": ManagerUser,
                "team_member": TeamMemberUser,
                "client": ClientUser,
            }[role]

            domain_user = domain_cls(
                name=login,
                email=f"{login}@example.com",
                role=role,
                login=login
            )

            # domain -> Django ORM
            created_user = user_repo.save(domain_user, password="test123")

            users[role] = created_user

        print("Users OK!")

        # PROJECTS
        project1 = ProjectBase("Website Redesign", "Redesign company website")
        project1.add_member_id(users["manager"].get_id())
        project1.add_member_id(users["team_member"].get_id())
        project_repo.save(project1)

        project2 = ProjectBase("Mobile App", "Develop mobile application")
        project2.add_member_id(users["manager"].get_id())
        project2.add_member_id(users["team_member"].get_id())
        project_repo.save(project2)

        # SPRINTS
        sprint1 = SprintBase(
            sprint_id=str(uuid.uuid4()),
            name="Sprint 1",
            start_date=datetime.now(),
            end_date=datetime.now() + timedelta(days=14),
            project_id=project1.get_id()
        )
        sprint_repo.save(sprint1)

        # TASKS
        task1 = BugTask(
            title="Fix login bug",
            description="Cannot login",
            task_id=str(uuid.uuid4()),
            severity="high"
        )
        task1.assign_user_id(users["team_member"].get_id())
        task_repo.save(task1)

        print("Seeding complete!")