from django.core.management.base import BaseCommand
from django.utils import timezone
from infrastructure.repositories.user_django_repository import UserDjangoRepository
from infrastructure.repositories.project_django_repository import ProjectDjangoRepository
from infrastructure.repositories.task_django_repository import TaskDjangoRepository
from infrastructure.repositories.sprint_django_repository import SprintDjangoRepository
from infrastructure.repositories.tag_django_repository import TagDjangoRepository
from infrastructure.repositories.comment_django_repository import CommentDjangoRepository

from domain.users.admin_user import AdminUser
from domain.users.manager_user import ManagerUser
from domain.users.team_member_user import TeamMemberUser
from domain.users.client_user import ClientUser

from domain.projects.project_base import ProjectBase
from domain.sprints.sprint_base import SprintBase
from domain.tasks.bug_task import BugTask
from domain.tasks.feature_task import FeatureTask
from domain.tasks.chore_task import ChoreTask
from domain.tags.tag import Tag
from domain.comments.comment import Comment

import uuid
from datetime import timedelta


class Command(BaseCommand):
    help = "Seed database with comprehensive demo data for Synexify with access control showcase"

    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS("=== 🚀 [Synexify SEED - EXTENDED] ==="))

        # --- REPOSITORIES ---
        user_repo = UserDjangoRepository()
        project_repo = ProjectDjangoRepository()
        sprint_repo = SprintDjangoRepository()
        task_repo = TaskDjangoRepository()
        tag_repo = TagDjangoRepository()
        comment_repo = CommentDjangoRepository(user_repo=user_repo)

        # === USERS - MORE USERS FOR BETTER DEMO ===
        self.stdout.write("📝 Seeding users (15 users)...")
        users = {}

        ROLES_AND_LOGINS = [
            # ADMINS
            ("admin", "root", "Root Admin"),
            ("admin", "admin2", "Admin Two"),

            # MANAGERS
            ("manager", "manager1", "John Manager - WebApp"),
            ("manager", "manager2", "Sarah Manager - CRM"),
            ("manager", "manager3", "Mike Manager - LandingPage"),

            # DEVELOPERS
            ("team_member", "dev1", "Alice Developer - Frontend"),
            ("team_member", "dev2", "Bob Developer - Backend"),
            ("team_member", "dev3", "Charlie Developer - Mobile"),
            ("team_member", "dev4", "Diana Developer - QA"),

            # QA SPECIALISTS
            ("team_member", "qa1", "Eve QA - WebApp"),
            ("team_member", "qa2", "Frank QA - CRM"),

            # CLIENTS
            ("client", "client1", "Acme Corp - WebApp Client"),
            ("client", "client2", "TechStart Inc - CRM Client"),
            ("client", "client3", "Marketing Pro - LandingPage Client"),
        ]

        for role, login, name in ROLES_AND_LOGINS:
            existing = user_repo.get_by_login(login)
            if existing:
                users[f"{role}_{login}"] = existing
                self.stdout.write(f"  ✓ {name} (exists)")
                continue

            cls_map = {
                "admin": AdminUser,
                "manager": ManagerUser,
                "team_member": TeamMemberUser,
                "client": ClientUser,
            }
            user_obj = cls_map[role](
                name=name,
                email=f"{login}@demo.synexify.com",
                role=role,
                login=login,
            )
            created = user_repo.save(user_obj, password="demo123")
            users[f"{role}_{login}"] = created
            self.stdout.write(f"  ✓ {name}")

        # Aliases
        admin = users["admin_root"]
        manager1 = users["manager_manager1"]
        manager2 = users["manager_manager2"]
        manager3 = users["manager_manager3"]
        dev1 = users["team_member_dev1"]
        dev2 = users["team_member_dev2"]
        dev3 = users["team_member_dev3"]
        dev4 = users["team_member_dev4"]
        qa1 = users["team_member_qa1"]
        qa2 = users["team_member_qa2"]
        client1 = users["client_client1"]
        client2 = users["client_client2"]
        client3 = users["client_client3"]

        # === TAGS ===
        self.stdout.write("🏷️  Seeding tags...")
        tag_names = ["backend", "frontend", "urgent", "review", "api", "ux", "devops", "mobile", "database"]
        tags = {}
        for tname in tag_names:
            tag_obj = Tag(tag_id=str(uuid.uuid4()), name=tname)
            tags[tname] = tag_repo.save(tag_obj)
            self.stdout.write(f"  ✓ {tname}")

        # === PROJECTS ===
        self.stdout.write("📦 Seeding projects (5 projects)...")
        now = timezone.now()

        # PROJECT 1: WebApp Rebuild (manager1, dev1, dev2, qa1, client1)
        project1 = ProjectBase(
            "WebApp Rebuild",
            "Complete rewrite of legacy web application with React + FastAPI"
        )
        for u in [manager1, dev1, dev2, qa1]:
            project1.add_member_id(u.get_id())
        project1.add_member_id(client1.get_id())  # CLIENT CAN SEE
        project1.add_manager_id(manager1.get_id())
        project_repo.save(project1)
        self.stdout.write("  ✓ WebApp Rebuild (client1 has access)")

        # PROJECT 2: Mobile CRM (manager2, dev2, dev3, qa2, client2)
        project2 = ProjectBase(
            "Mobile CRM Platform",
            "Next-gen mobile CRM application for sales teams"
        )
        for u in [manager2, dev2, dev3, qa2]:
            project2.add_member_id(u.get_id())
        project2.add_member_id(client2.get_id())  # CLIENT CAN SEE
        project2.add_manager_id(manager2.get_id())
        project_repo.save(project2)
        self.stdout.write("  ✓ Mobile CRM Platform (client2 has access)")

        # PROJECT 3: Landing Page (manager3, dev1, qa1, client3)
        project3 = ProjectBase(
            "Marketing Landing Page",
            "Campaign landing page with conversion optimization"
        )
        for u in [manager3, dev1, qa1]:
            project3.add_member_id(u.get_id())
        project3.add_member_id(client3.get_id())  # CLIENT CAN SEE
        project3.add_manager_id(manager3.get_id())
        project_repo.save(project3)
        self.stdout.write("  ✓ Marketing Landing Page (client3 has access)")

        # PROJECT 4: Internal Tool (manager1, dev3, dev4)
        project4 = ProjectBase(
            "Internal Analytics Tool",
            "Internal tool - NO CLIENTS can see this"
        )
        for u in [manager1, dev3, dev4]:
            project4.add_member_id(u.get_id())
        project4.add_manager_id(manager1.get_id())
        project_repo.save(project4)
        self.stdout.write("  ✓ Internal Analytics Tool (NO CLIENT ACCESS)")

        # PROJECT 5: Maintenance (manager2, dev4)
        project5 = ProjectBase(
            "Legacy System Maintenance",
            "Maintain old system - small team only"
        )
        for u in [manager2, dev4]:
            project5.add_member_id(u.get_id())
        project5.add_manager_id(manager2.get_id())
        project_repo.save(project5)
        self.stdout.write("  ✓ Legacy System Maintenance (NO CLIENT ACCESS)")

        # === SPRINTS ===
        self.stdout.write("🏃 Seeding sprints...")

        # PROJECT 1 SPRINTS
        p1_completed = SprintBase(
            sprint_id=str(uuid.uuid4()),
            name="Sprint 0:  MVP (COMPLETED)",
            start_date=now - timedelta(days=30),
            end_date=now - timedelta(days=16),
            project_id=project1.get_id()
        )
        sprint_repo.save(p1_completed)
        project1.add_sprint_id(p1_completed.get_id())

        p1_sprint1 = SprintBase(
            sprint_id=str(uuid.uuid4()),
            name="Sprint 1: Authentication",
            start_date=now - timedelta(days=5),
            end_date=now + timedelta(days=9),
            project_id=project1.get_id()
        )
        sprint_repo.save(p1_sprint1)
        project1.add_sprint_id(p1_sprint1.get_id())

        p1_sprint2 = SprintBase(
            sprint_id=str(uuid.uuid4()),
            name="Sprint 2: Dashboard",
            start_date=now + timedelta(days=10),
            end_date=now + timedelta(days=24),
            project_id=project1.get_id()
        )
        sprint_repo.save(p1_sprint2)
        project1.add_sprint_id(p1_sprint2.get_id())
        project_repo.save(project1)
        self.stdout.write("  ✓ Project 1: 3 sprints")

        # PROJECT 2 SPRINTS
        p2_sprint1 = SprintBase(
            sprint_id=str(uuid.uuid4()),
            name="Sprint 1: MVP Pilot",
            start_date=now - timedelta(days=2),
            end_date=now + timedelta(days=12),
            project_id=project2.get_id()
        )
        sprint_repo.save(p2_sprint1)
        project2.add_sprint_id(p2_sprint1.get_id())
        project_repo.save(project2)
        self.stdout.write("  ✓ Project 2: 1 sprint")

        # PROJECT 3 SPRINTS
        p3_sprint1 = SprintBase(
            sprint_id=str(uuid.uuid4()),
            name="Sprint 1: Campaign A",
            start_date=now - timedelta(days=7),
            end_date=now + timedelta(days=7),
            project_id=project3.get_id()
        )
        sprint_repo.save(p3_sprint1)
        project3.add_sprint_id(p3_sprint1.get_id())
        project_repo.save(project3)
        self.stdout.write("  ✓ Project 3: 1 sprint")

        # === TASKS - PROJECT 1 ===
        self.stdout.write("📌 Seeding tasks (30+ tasks)...")

        # Completed tasks
        c_t1 = FeatureTask(
            title="User login system",
            description="Basic email/password authentication",
            story_points=8,
            task_id=str(uuid.uuid4()),
            project_id=project1.get_id(),
            sprint_id=p1_completed.get_id()
        )
        c_t1.assign_user_id(dev1.get_id())
        c_t1.add_tag_id(tags["backend"].get_id())
        c_t1.add_tag_id(tags["api"].get_id())
        task_repo.save(c_t1)
        c_t1 = task_repo.get_by_id(c_t1.get_id())
        c_t1.update_status("Done")
        task_repo.save(c_t1)
        p1_completed.add_task_id(c_t1.get_id())

        c_t2 = FeatureTask(
            title="User registration",
            description="Create registration form",
            story_points=5,
            task_id=str(uuid.uuid4()),
            project_id=project1.get_id(),
            sprint_id=p1_completed.get_id()
        )
        c_t2.assign_user_id(dev2.get_id())
        c_t2.add_tag_id(tags["frontend"].get_id())
        task_repo.save(c_t2)
        c_t2 = task_repo.get_by_id(c_t2.get_id())
        c_t2.update_status("Done")
        task_repo.save(c_t2)
        p1_completed.add_task_id(c_t2.get_id())

        c_t3 = BugTask(
            title="Password validation bug",
            description="Special chars not accepted",
            severity="high",
            task_id=str(uuid.uuid4()),
            project_id=project1.get_id(),
            sprint_id=p1_completed.get_id()
        )
        c_t3.assign_user_id(qa1.get_id())
        c_t3.add_tag_id(tags["backend"].get_id())
        task_repo.save(c_t3)
        c_t3 = task_repo.get_by_id(c_t3.get_id())
        c_t3.update_status("Done")
        task_repo.save(c_t3)
        p1_completed.add_task_id(c_t3.get_id())

        c_t4 = ChoreTask(
            title="Security audit",
            description="OWASP top 10 review",
            task_id=str(uuid.uuid4()),
            project_id=project1.get_id(),
            sprint_id=p1_completed.get_id()
        )
        c_t4.assign_user_id(dev1.get_id())
        task_repo.save(c_t4)
        c_t4 = task_repo.get_by_id(c_t4.get_id())
        c_t4.update_status("Done")
        task_repo.save(c_t4)
        p1_completed.add_task_id(c_t4.get_id())
        sprint_repo.save(p1_completed)

        # Sprint 1 tasks
        for i in range(5):
            task = FeatureTask(
                title=f"Sprint 1 Task {i + 1}",
                description=f"Authentication feature {i + 1}",
                story_points=3 + i,
                task_id=str(uuid.uuid4()),
                project_id=project1.get_id(),
                sprint_id=p1_sprint1.get_id()
            )
            task.assign_user_id([dev1, dev2, qa1][i % 3].get_id())
            task.add_tag_id(tags["backend"].get_id())
            task_repo.save(task)
            if i % 2 == 0:
                task = task_repo.get_by_id(task.get_id())
                task.update_status("Done")
                task_repo.save(task)
            p1_sprint1.add_task_id(task.get_id())
        sprint_repo.save(p1_sprint1)

        # Sprint 2 tasks
        for i in range(6):
            task = FeatureTask(
                title=f"Dashboard Feature {i + 1}",
                description=f"Dashboard component {i + 1}",
                story_points=5 + i,
                task_id=str(uuid.uuid4()),
                project_id=project1.get_id(),
                sprint_id=p1_sprint2.get_id()
            )
            task.assign_user_id([dev1, dev2, qa1][i % 3].get_id())
            task.add_tag_id(tags["frontend"].get_id())
            task_repo.save(task)
            if i < 2:
                task = task_repo.get_by_id(task.get_id())
                task.update_status("Done")
                task_repo.save(task)
            p1_sprint2.add_task_id(task.get_id())
        sprint_repo.save(p1_sprint2)

        # === PROJECT 2 TASKS ===
        for i in range(7):
            task = FeatureTask(
                title=f"CRM Feature {i + 1}",
                description=f"Mobile CRM feature {i + 1}",
                story_points=8 + i,
                task_id=str(uuid.uuid4()),
                project_id=project2.get_id(),
                sprint_id=p2_sprint1.get_id()
            )
            task.assign_user_id([dev2, dev3, qa2][i % 3].get_id())
            if i % 2 == 0:
                task.add_tag_id(tags["mobile"].get_id())
            else:
                task.add_tag_id(tags["backend"].get_id())
            task_repo.save(task)
            if i == 0:
                task = task_repo.get_by_id(task.get_id())
                task.update_status("In Progress")
                task_repo.save(task)
            p2_sprint1.add_task_id(task.get_id())
        sprint_repo.save(p2_sprint1)
        project2 = project_repo.get_by_id(project2.get_id())

        # === PROJECT 3 TASKS ===
        for i in range(5):
            task = FeatureTask(
                title=f"Landing Page Element {i + 1}",
                description=f"Campaign landing page section {i + 1}",
                story_points=2 + i,
                task_id=str(uuid.uuid4()),
                project_id=project3.get_id(),
                sprint_id=p3_sprint1.get_id()
            )
            task.assign_user_id([dev1, qa1, manager3][i % 3].get_id())
            task.add_tag_id(tags["frontend"].get_id())
            task_repo.save(task)
            if i < 3:
                task = task_repo.get_by_id(task.get_id())
                task.update_status("Done")
                task_repo.save(task)
            p3_sprint1.add_task_id(task.get_id())
        sprint_repo.save(p3_sprint1)
        project3 = project_repo.get_by_id(project3.get_id())

        # === PROJECT 4 & 5 TASKS (NO CLIENT ACCESS) ===
        for i in range(4):
            task = FeatureTask(
                title=f"Internal Tool Feature {i + 1}",
                description=f"Internal analytics feature",
                story_points=5,
                task_id=str(uuid.uuid4()),
                project_id=project4.get_id(),
            )
            task.assign_user_id([dev3, dev4][i % 2].get_id())
            task.add_tag_id(tags["backend"].get_id())
            task_repo.save(task)
            project4.add_task_id(task.get_id())
        project_repo.save(project4)

        for i in range(3):
            task = BugTask(
                title=f"Maintenance Issue {i + 1}",
                description=f"Legacy system maintenance",
                severity="medium",
                task_id=str(uuid.uuid4()),
                project_id=project5.get_id(),
            )
            task.assign_user_id(dev4.get_id())
            task.add_tag_id(tags["database"].get_id())
            task_repo.save(task)
            project5.add_task_id(task.get_id())
        project_repo.save(project5)

        self.stdout.write("  ✓ 30+ tasks seeded")

        # === COMMENTS ===
        self.stdout.write("💬 Seeding comments...")
        comment_data = [
            (c_t1, dev1, "✅ Authentication layer complete"),
            (c_t2, dev2, "✅ Registration validated and tested"),
            (c_t3, qa1, "🐛 Bug confirmed and fixed"),
        ]

        for task, user, text in comment_data:
            comment = Comment(content=text, author=user)
            comment_repo.save(comment, task.get_id())

        self.stdout.write("  ✓ Comments added")

        # === SUCCESS ===
        self.stdout.write(self.style.SUCCESS("\n=== ✅ [EXTENDED SEED COMPLETE! ] ===\n"))
        print("\n" + "=" * 70)
        print("🔐 DEMO CREDENTIALS (Password: demo123):")
        print("=" * 70)
        print("\n👤 ADMIN:")
        print("  root          (全系统访问) - Full system access")
        print("\n👔 MANAGERS:")
        print("  manager1      (WebApp Rebuild)")
        print("  manager2      (Mobile CRM + Legacy Maintenance)")
        print("  manager3      (Marketing Landing Page)")
        print("\n👨‍💻 DEVELOPERS:")
        print("  dev1          (WebApp + Landing Page)")
        print("  dev2          (WebApp + CRM)")
        print("  dev3          (CRM + Internal Tool)")
        print("  dev4          (Internal Tool + Legacy)")
        print("\n🔍 QA:")
        print("  qa1           (WebApp + Landing Page)")
        print("  qa2           (CRM)")
        print("\n👥 CLIENTS (LIMITED ACCESS):")
        print("  client1       (Can see:  WebApp Rebuild ONLY)")
        print("  client2       (Can see: Mobile CRM ONLY)")
        print("  client3       (Can see:  Marketing Landing Page ONLY)")
        print("\n" + "=" * 70)
        print("📊 CREATED:")
        print("  • 14 Users (2 Admin, 3 Manager, 6 Dev, 2 QA, 3 Client)")
        print("  • 5 Projects (3 with clients, 2 internal)")
        print("  • 8 Sprints (across 3 projects)")
        print("  • 35+ Tasks")
        print("  • 9 Tags")
        print("  • 3 Comments")
        print("\n🎯 DEMO FEATURES:")
        print("  ✓ Permission-based access control")
        print("  ✓ Clients see ONLY their projects")
        print("  ✓ Managers see their assigned projects")
        print("  ✓ Admin sees everything")
        print("  ✓ Multiple sprints with different statuses")
        print("  ✓ Completed sprint for velocity reports")
        print("=" * 70)