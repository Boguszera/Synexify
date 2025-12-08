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
        role_map = [
            ("admin", "root"),
            ("manager", "mgr1"),
            ("team_member", "member1"),
            ("client", "client1")
        ]

        for role, login in role_map:
            existing_user = user_repo.get_by_login(login)
            if existing_user:
                print(f"User {login} already exists, skipping...")
                users[role] = existing_user
                continue

            if role == "admin":
                user = AdminUser(name=login, email=f"{login}@example.com", role=role, login=login)
            elif role == "manager":
                user = ManagerUser(name=login, email=f"{login}@example.com", role=role, login=login)
            elif role == "team_member":
                user = TeamMemberUser(name=login, email=f"{login}@example.com", role=role, login=login)
            else:
                user = ClientUser(name=login, email=f"{login}@example.com", role=role, login=login)

            user_repo.save(user)
            users[role] = user

        # --- PROJECTS ---
        print("Creating projects...")

        def create_project_if_not_exists(name, description, member_ids):
            # Sprawdź po nazwie, czy projekt już istnieje
            existing = next((p for p in project_repo.list_all() if p.get_name() == name), None)
            if existing:
                print(f"Project {name} already exists, skipping...")
                return existing
            proj = ProjectBase(name=name, description=description)
            for uid in member_ids:
                proj.add_member_id(uid)
            project_repo.save(proj)
            return proj

        project1 = create_project_if_not_exists(
            "Website Redesign", "Redesign company website",
            [users["manager"].get_id(), users["team_member"].get_id()]
        )

        project2 = create_project_if_not_exists(
            "Mobile App", "Develop mobile application",
            [users["manager"].get_id(), users["team_member"].get_id()]
        )

        # --- SPRINTS ---
        print("Creating sprints...")

        def create_sprint_if_not_exists(name, start_date, end_date, project):
            existing = next(
                (s for s in sprint_repo.list_by_project(project.get_id()) if s.get_name() == name),
                None
            )
            if existing:
                print(f"Sprint {name} already exists in project {project.get_name()}, skipping...")
                return existing
            sprint = SprintBase(
                sprint_id=str(uuid.uuid4()),
                name=name,
                start_date=start_date,
                end_date=end_date,
                project_id=project.get_id()
            )
            project.add_sprint_id(sprint.get_id())
            project_repo.save(project)
            sprint_repo.save(sprint)
            return sprint

        sprint1 = create_sprint_if_not_exists(
            "Sprint 1", datetime.now(), datetime.now() + timedelta(days=14), project1
        )

        sprint2 = create_sprint_if_not_exists(
            "Sprint 2", datetime.now() + timedelta(days=15), datetime.now() + timedelta(days=30), project1
        )

        # --- TASKS ---
        print("Creating tasks...")

        def create_task_if_not_exists(task_class, title, description, assignee_id, project, sprint=None, **kwargs):
            existing = next(
                (t for t in task_repo.get_all() if t.get_title() == title),
                None
            )
            if existing:
                print(f"Task {title} already exists, skipping...")
                return existing
            task = task_class(title=title, description=description, task_id=str(uuid.uuid4()), **kwargs)
            task.assign_user_id(assignee_id)
            project.add_task_id(task.get_id())
            if sprint:
                sprint.add_task_id(task.get_id())
            task_repo.save(task)
            project_repo.save(project)
            if sprint:
                sprint_repo.save(sprint)
            return task

        task1 = create_task_if_not_exists(
            BugTask, "Fix login bug",
            "Cannot login with correct credentials",
            users["team_member"].get_id(),
            project1,
            sprint1,
            severity="high"
        )

        task2 = create_task_if_not_exists(
            FeatureTask, "Add user profile page",
            "Create profile page for users",
            users["team_member"].get_id(),
            project1,
            sprint1,
            story_points=5
        )

        task3 = create_task_if_not_exists(
            ChoreTask, "Setup CI/CD",
            "Configure GitHub Actions pipelines",
            users["manager"].get_id(),
            project2
        )

        # --- COMMENTS ---
        print("Adding comments...")

        def add_comment_to_task(task, content, author):
            existing_comments = [c_id for c_id in task.get_comments_ids()]
            if existing_comments:
                print(f"Task {task.get_id()} already has comments, skipping...")
                return
            comment = Comment(content=content, author=author)
            task.add_comment(comment.get_id(), comment.get_author())
            task_repo.save(task)

        add_comment_to_task(task1, "Started working on bug", users["team_member"])
        add_comment_to_task(task2, "Remember to add tests", users["manager"])

        # --- ATTACHMENTS ---
        print("Adding attachments...")

        def add_attachment_to_task(task, filename, uploader):
            existing_attachments = [a_id for a_id in task.get_attachment_ids()]
            if existing_attachments:
                print(f"Task {task.get_id()} already has attachments, skipping...")
                return
            attachment = Attachment(filename=filename, uploaded_by=uploader)
            task.attach_file_id(attachment.get_id())
            task_repo.save(task)

        add_attachment_to_task(task1, "screenshot.png", users["team_member"])

        print("Seeding complete!")
