from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from infrastructure.repositories.user_django_repository import UserDjangoRepository
from infrastructure.repositories.project_django_repository import ProjectDjangoRepository
from infrastructure.repositories.task_django_repository import TaskDjangoRepository
from infrastructure.repositories.sprint_django_repository import SprintDjangoRepository
from domain.sprints.sprint_base import SprintBase
from domain.users.admin_user import AdminUser
from domain.users.manager_user import ManagerUser
from domain.users.team_member_user import TeamMemberUser
from domain.users.client_user import ClientUser
from domain.projects.project_base import ProjectBase
from domain.tasks.bug_task import BugTask
from domain.tasks.feature_task import FeatureTask
from domain.tasks.chore_task import ChoreTask
from domain.comments.comment import Comment
from domain.attachments.attachment import Attachment
from datetime import datetime, timedelta
import uuid

class Command(BaseCommand):
    help = "Seed database with users, projects, sprints, tasks, comments, attachments"

    def handle(self, *args, **options):
        print("Seeding data...")

        user_repo = UserDjangoRepository()
        project_repo = ProjectDjangoRepository()
        sprint_repo = SprintDjangoRepository()
        task_repo = TaskDjangoRepository()

        # --- USERS ---
        print("Creating users...")
        users = {}

        for role, login in [("admin", "root"), ("manager", "mgr1"), ("team_member", "member1"), ("client", "client1")]:
            if role == "admin":
                user = AdminUser(name=login, email=f"{login}@example.com", role=role, login=login)
            elif role == "manager":
                user = ManagerUser(name=login, email=f"{login}@example.com", role=role, login=login)
            elif role == "team_member":
                user = TeamMemberUser(name=login, email=f"{login}@example.com", role=role, login=login)
            else:
                user = ClientUser(name=login, email=f"{login}@example.com", role=role, login=login)

            user_repo.save(user)
            users[login] = user

            User.objects.update_or_create(
                username=user.get_login(),
                defaults={"email": user.get_email(), "password": "zaq1@WSX"}
            )

        # --- PROJECT ---
        print("Creating projects...")
        project1 = ProjectBase(name="Website Redesign", description="Redesign company website")
        project1.add_member_id(users["manager"].get_id())
        project1.add_member_id(users["team_member"].get_id())
        project_repo.save(project1)

        project2 = ProjectBase(name="Mobile App", description="Develop mobile application")
        project2.add_member_id(users["manager"].get_id())
        project2.add_member_id(users["team_member"].get_id())
        project_repo.save(project2)

        # --- SPRINTS ---
        print("Creating sprints...")
        sprint1 = SprintBase(sprint_id=1, name="Sprint 1", start_date=datetime.now(),
                             end_date=datetime.now() + timedelta(days=14))
        sprint2 = SprintBase(sprint_id=2, name="Sprint 2", start_date=datetime.now() + timedelta(days=15),
                             end_date=datetime.now() + timedelta(days=30))
        sprint_repo.save(sprint1)
        sprint_repo.save(sprint2)
        project1.add_sprint_id(sprint1.get_id())
        project1.add_sprint_id(sprint2.get_id())
        project_repo.save(project1)

        # --- TASKS ---
        print("Creating tasks...")
        task1 = BugTask(title="Fix login bug", description="Cannot login with correct credentials", severity="high", task_id=str(uuid.uuid4()))
        task1.assign_user_id(users["team_member"].get_id())
        project1.add_task_id(task1.get_id())
        sprint1.add_task_id(task1.get_id())
        task_repo.save(task1)

        task2 = FeatureTask(title="Add user profile page", description="Create profile page for users", story_points=5, task_id=str(uuid.uuid4()))
        task2.assign_user_id(users["team_member"].get_id())
        project1.add_task_id(task2.get_id())
        sprint1.add_task_id(task2.get_id())
        task_repo.save(task2)

        task3 = ChoreTask(title="Setup CI/CD", description="Configure GitHub Actions pipelines", task_id=str(uuid.uuid4()))
        task3.assign_user_id(users["manager"].get_id())
        project2.add_task_id(task3.get_id())
        task_repo.save(task3)

        project_repo.save(project1)
        project_repo.save(project2)

        # --- COMMENTS ---
        print("Adding comments...")
        comment1 = Comment(content="Started working on bug", author=users["team_member"])
        task1.add_comment(comment1.get_id(), comment1.get_author())
        task_repo.save(task1)

        comment2 = Comment(content="Remember to add tests", author=users["manager"])
        task2.add_comment(comment2.get_id(), comment2.get_author())
        task_repo.save(task2)

        # --- ATTACHMENTS ---
        print("Adding attachments...")
        attachment1 = Attachment(filename="screenshot.png", uploaded_by=users["team_member"])
        task1.attach_file_id(attachment1.get_id())
        task_repo.save(task1)

        print("Seeding complete!")
