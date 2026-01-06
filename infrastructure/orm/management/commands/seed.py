from django.core.management.base import BaseCommand
from django.utils import timezone
from infrastructure.repositories.user_django_repository import UserDjangoRepository
from infrastructure.repositories. project_django_repository import ProjectDjangoRepository
from infrastructure.repositories.task_django_repository import TaskDjangoRepository
from infrastructure.repositories. sprint_django_repository import SprintDjangoRepository
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
    help = "Seed database with comprehensive demo data for Synexify including completed sprints"

    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS("=== 🚀 [Synexify SEED] ==="))

        # --- REPOSITORIES ---
        user_repo = UserDjangoRepository()
        project_repo = ProjectDjangoRepository()
        sprint_repo = SprintDjangoRepository()
        task_repo = TaskDjangoRepository()
        tag_repo = TagDjangoRepository()
        comment_repo = CommentDjangoRepository(user_repo=user_repo)

        # === USERS ===
        self.stdout.write("📝 Seeding users...")
        users = {}
        ROLES_AND_LOGINS = [
            ("admin", "root", "Admin User"),
            ("manager", "manager1", "John Manager"),
            ("team_member", "dev1", "Alice Developer"),
            ("team_member", "dev2", "Bob Developer"),
            ("team_member", "qa1", "Charlie QA"),
            ("client", "client1", "Client Customer"),
        ]

        for role, login, name in ROLES_AND_LOGINS:
            existing = user_repo.get_by_login(login)
            if existing:
                users[f"{role}_{login}"] = existing
                self.stdout.write(f"  ✓ {name} (already exists)")
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
            self.stdout.write(f"  ✓ {name} ({role})")

        # Aliases
        admin = users["admin_root"]
        manager = users["manager_manager1"]
        dev1 = users["team_member_dev1"]
        dev2 = users["team_member_dev2"]
        qa = users["team_member_qa1"]
        client = users["client_client1"]

        # === TAGS ===
        self.stdout. write("🏷️  Seeding tags...")
        tag_names = ["backend", "frontend", "urgent", "review", "api", "ux", "devops"]
        tags = {}
        for tname in tag_names:
            tag_obj = Tag(tag_id=str(uuid.uuid4()), name=tname)
            tags[tname] = tag_repo.save(tag_obj)
            self.stdout.write(f"  ✓ {tname}")

        # === PROJECTS ===
        self.stdout. write("📦 Seeding projects...")
        now = timezone.now()

        # PROJECT 1: WebApp Rebuild
        project1 = ProjectBase(
            "WebApp Rebuild",
            "Complete rewrite of legacy web application with modern stack (React + FastAPI)"
        )
        for u in [manager, dev1, dev2, qa]:
            project1.add_member_id(u.get_id())
        project1.add_manager_id(manager.get_id())
        project1.add_manager_id(admin.get_id())
        project_repo.save(project1)
        self.stdout.write("  ✓ WebApp Rebuild")

        # PROJECT 2: Mobile CRM
        project2 = ProjectBase(
            "Mobile CRM Platform",
            "Next-gen mobile CRM application for sales teams"
        )
        for u in [manager, dev1, client]:
            project2.add_member_id(u.get_id())
        project2.add_manager_id(manager.get_id())
        project_repo.save(project2)
        self.stdout.write("  ✓ Mobile CRM Platform")

        # PROJECT 3: Landing Page
        project3 = ProjectBase(
            "Marketing Landing Page",
            "Campaign landing page with conversion optimization"
        )
        for u in [manager, dev2, client]:
            project3.add_member_id(u. get_id())
        project3.add_manager_id(manager.get_id())
        project_repo.save(project3)
        self.stdout.write("  ✓ Marketing Landing Page")

        # === SPRINTS ===
        self.stdout.write("🏃 Seeding sprints...")

        # COMPLETED SPRINT (dla Team Velocity!)
        completed_sprint = SprintBase(
            sprint_id=str(uuid.uuid4()),
            name="Sprint 0:  MVP (COMPLETED)",
            start_date=now - timedelta(days=30),
            end_date=now - timedelta(days=16),
            project_id=project1.get_id()
        )
        sprint_repo.save(completed_sprint)
        project1.add_sprint_id(completed_sprint.get_id())
        self.stdout. write("  ✓ Sprint 0 (COMPLETED)")

        # WebApp Sprints (Active)
        sprint1 = SprintBase(
            sprint_id=str(uuid.uuid4()),
            name="Sprint 1: Authentication",
            start_date=now - timedelta(days=5),
            end_date=now + timedelta(days=9),
            project_id=project1.get_id()
        )
        sprint2 = SprintBase(
            sprint_id=str(uuid.uuid4()),
            name="Sprint 2: Dashboard & Analytics",
            start_date=now + timedelta(days=10),
            end_date=now + timedelta(days=24),
            project_id=project1.get_id()
        )
        sprint_repo.save(sprint1)
        sprint_repo.save(sprint2)
        project1.add_sprint_id(sprint1.get_id())
        project1.add_sprint_id(sprint2.get_id())
        project_repo.save(project1)
        self.stdout.write("  ✓ WebApp:  Sprint 1 & 2")

        # CRM Sprint
        sprint3 = SprintBase(
            sprint_id=str(uuid.uuid4()),
            name="Sprint 1:  Pilot MVP",
            start_date=now - timedelta(days=2),
            end_date=now + timedelta(days=12),
            project_id=project2.get_id()
        )
        sprint_repo.save(sprint3)
        project2.add_sprint_id(sprint3.get_id())
        project_repo.save(project2)
        self.stdout.write("  ✓ CRM:  Sprint 1")

        # === TASKS - COMPLETED SPRINT ===
        self.stdout. write("📌 Seeding tasks (COMPLETED SPRINT)...")

        # Te taski mają być DONE (dla Team Velocity)
        completed_tasks = []

        c_t1 = FeatureTask(
            title="User login system",
            description="Implement basic login with email/password",
            story_points=8,
            task_id=str(uuid.uuid4()),
            project_id=project1.get_id(),
            sprint_id=completed_sprint.get_id()
        )
        c_t1.assign_user_id(dev1.get_id())
        c_t1.add_tag_id(tags["backend"].get_id())
        c_t1.add_tag_id(tags["api"].get_id())
        task_repo.save(c_t1)
        c_t1 = task_repo.get_by_id(c_t1.get_id())
        c_t1.update_status("Done")
        task_repo.save(c_t1)
        completed_sprint.add_task_id(c_t1.get_id())
        completed_tasks.append(c_t1)

        c_t2 = FeatureTask(
            title="User registration",
            description="Create registration form with validation",
            story_points=5,
            task_id=str(uuid.uuid4()),
            project_id=project1.get_id(),
            sprint_id=completed_sprint.get_id()
        )
        c_t2.assign_user_id(dev2.get_id())
        c_t2.add_tag_id(tags["frontend"].get_id())
        task_repo.save(c_t2)
        c_t2 = task_repo.get_by_id(c_t2.get_id())
        c_t2.update_status("Done")
        task_repo.save(c_t2)
        completed_sprint.add_task_id(c_t2.get_id())
        completed_tasks.append(c_t2)

        c_t3 = BugTask(
            title="Password validation bug",
            description="Special chars not accepted in password",
            severity="high",
            task_id=str(uuid.uuid4()),
            project_id=project1.get_id(),
            sprint_id=completed_sprint.get_id()
        )
        c_t3.assign_user_id(qa.get_id())
        c_t3.add_tag_id(tags["backend"].get_id())
        task_repo.save(c_t3)
        c_t3 = task_repo.get_by_id(c_t3.get_id())
        c_t3.update_status("Done")
        task_repo.save(c_t3)
        completed_sprint.add_task_id(c_t3.get_id())
        completed_tasks.append(c_t3)

        c_t4 = ChoreTask(
            title="Security audit",
            description="Check for OWASP top 10",
            task_id=str(uuid.uuid4()),
            project_id=project1.get_id(),
            sprint_id=completed_sprint.get_id()
        )
        c_t4.assign_user_id(dev1.get_id())
        task_repo.save(c_t4)
        c_t4 = task_repo.get_by_id(c_t4.get_id())
        c_t4.update_status("Done")
        task_repo.save(c_t4)
        completed_sprint.add_task_id(c_t4.get_id())
        completed_tasks.append(c_t4)

        sprint_repo.save(completed_sprint)
        project1 = project_repo.get_by_id(project1.get_id())
        self.stdout.write(f"  ✓ Completed Sprint: 4 tasks (13 + 5 + 0 + 0 = 18 story points)")

        # === TASKS - ACTIVE SPRINTS ===
        self.stdout.write("📌 Seeding tasks (ACTIVE SPRINTS)...")

        # SPRINT 1
        t5 = FeatureTask(
            title="Password reset via email",
            description="Send reset link with 24h token expiry, validate and update password securely",
            story_points=3,
            task_id=str(uuid.uuid4()),
            project_id=project1.get_id(),
            sprint_id=sprint1.get_id()
        )
        t5.assign_user_id(dev1.get_id())
        t5.assign_user_id(dev2.get_id())
        t5.add_tag_id(tags["api"].get_id())
        task_repo.save(t5)
        t5 = task_repo.get_by_id(t5.get_id())
        t5.update_status("In Progress")
        task_repo.save(t5)
        sprint1.add_task_id(t5.get_id())

        t6 = BugTask(
            title="Broken button styles on IE11",
            description="Flexbox not working properly in legacy IE.  Need CSS fallbacks",
            severity="medium",
            task_id=str(uuid.uuid4()),
            project_id=project1.get_id(),
            sprint_id=sprint1.get_id()
        )
        t6.assign_user_id(qa. get_id())
        t6.add_tag_id(tags["frontend"].get_id())
        task_repo.save(t6)
        t6 = task_repo.get_by_id(t6.get_id())
        t6.update_status("Done")
        task_repo.save(t6)
        sprint1.add_task_id(t6.get_id())

        t7 = ChoreTask(
            title="Set up CI/CD pipeline",
            description="Configure GitHub Actions for automated tests and deployment",
            task_id=str(uuid.uuid4()),
            project_id=project1.get_id(),
            sprint_id=sprint1.get_id()
        )
        t7.assign_user_id(dev2.get_id())
        t7.add_tag_id(tags["devops"].get_id())
        task_repo.save(t7)
        t7 = task_repo.get_by_id(t7.get_id())
        t7.update_status("Done")
        task_repo.save(t7)
        sprint1.add_task_id(t7.get_id())

        sprint_repo.save(sprint1)

        # SPRINT 2
        t8 = FeatureTask(
            title="OAuth2 integration (Google & Azure)",
            description="Allow users to login with Google Account or Microsoft Azure AD credentials",
            story_points=8,
            task_id=str(uuid.uuid4()),
            project_id=project1.get_id(),
            sprint_id=sprint2.get_id()
        )
        t8.assign_user_id(dev2.get_id())
        t8.assign_user_id(manager.get_id())
        t8.add_tag_id(tags["backend"].get_id())
        t8.add_tag_id(tags["api"].get_id())
        task_repo.save(t8)
        t8 = task_repo.get_by_id(t8.get_id())
        t8.update_status("In Progress")
        task_repo.save(t8)
        sprint2.add_task_id(t8.get_id())

        t9 = FeatureTask(
            title="User dashboard mockup",
            description="Create responsive dashboard layout with chart placeholders",
            story_points=5,
            task_id=str(uuid.uuid4()),
            project_id=project1.get_id(),
            sprint_id=sprint2.get_id()
        )
        t9.assign_user_id(dev1.get_id())
        t9.add_tag_id(tags["frontend"].get_id())
        t9.add_tag_id(tags["ux"].get_id())
        task_repo.save(t9)
        sprint2.add_task_id(t9.get_id())

        t10 = BugTask(
            title="Dashboard loading too slow",
            description="Optimize queries, implement caching",
            severity="high",
            task_id=str(uuid.uuid4()),
            project_id=project1.get_id(),
            sprint_id=sprint2.get_id()
        )
        t10.assign_user_id(dev2.get_id())
        task_repo.save(t10)
        sprint2.add_task_id(t10.get_id())

        sprint_repo.save(sprint2)

        # CRM SPRINT
        crm1 = FeatureTask(
            title="Sales analytics dashboard",
            description="Interactive dashboard showing KPIs:  revenue, deals, pipeline",
            story_points=13,
            task_id=str(uuid.uuid4()),
            project_id=project2.get_id(),
        )
        crm1.assign_user_id(manager.get_id())
        crm1.assign_user_id(client.get_id())
        crm1.add_tag_id(tags["frontend"].get_id())
        crm1.add_tag_id(tags["review"].get_id())
        task_repo.save(crm1)
        project2.add_task_id(crm1.get_id())

        crm2 = BugTask(
            title="App crashes on Android 14",
            description="Critical:  App force closes on latest Android OS.  Likely memory leak or deprecated API usage",
            severity="critical",
            task_id=str(uuid.uuid4()),
            project_id=project2.get_id(),
            sprint_id=sprint3.get_id()
        )
        crm2.assign_user_id(dev1.get_id())
        crm2.add_tag_id(tags["backend"].get_id())
        crm2.add_tag_id(tags["urgent"].get_id())
        task_repo.save(crm2)
        crm2 = task_repo. get_by_id(crm2.get_id())
        crm2.update_status("In Progress")
        task_repo.save(crm2)
        sprint3.add_task_id(crm2.get_id())

        crm3 = FeatureTask(
            title="Offline mode for sales calls",
            description="Cache data locally so reps can work during calls without wifi",
            story_points=8,
            task_id=str(uuid.uuid4()),
            project_id=project2.get_id(),
            sprint_id=sprint3.get_id()
        )
        crm3.assign_user_id(dev1.get_id())
        crm3.add_tag_id(tags["backend"].get_id())
        task_repo.save(crm3)
        sprint3.add_task_id(crm3.get_id())

        sprint_repo.save(sprint3)
        project2 = project_repo.get_by_id(project2.get_id())

        # LANDING PAGE - backlog + completed
        lp1 = FeatureTask(
            title="Campaign popup with discount code",
            description="Popup appears once per user session with 20% discount offer",
            story_points=2,
            task_id=str(uuid.uuid4()),
            project_id=project3.get_id(),
        )
        lp1.assign_user_id(dev2.get_id())
        lp1.assign_user_id(client.get_id())
        lp1.add_tag_id(tags["frontend"].get_id())
        task_repo.save(lp1)
        project3.add_task_id(lp1.get_id())

        lp2 = ChoreTask(
            title="Verify Google Analytics tracking",
            description="Ensure conversion event fires when form is submitted",
            task_id=str(uuid.uuid4()),
            project_id=project3.get_id(),
        )
        lp2.assign_user_id(manager.get_id())
        task_repo.save(lp2)
        lp2 = task_repo.get_by_id(lp2.get_id())
        lp2.update_status("Done")
        task_repo.save(lp2)
        project3.add_task_id(lp2.get_id())

        lp3 = BugTask(
            title="Contact form not sending emails",
            description="SMTP configuration issue - emails stuck in queue",
            severity="high",
            task_id=str(uuid.uuid4()),
            project_id=project3.get_id(),
        )
        lp3.assign_user_id(dev2.get_id())
        lp3.add_tag_id(tags["backend"].get_id())
        lp3.add_tag_id(tags["urgent"].get_id())
        task_repo.save(lp3)
        project3.add_task_id(lp3.get_id())

        project_repo.save(project3)

        # === COMMENTS ===
        self.stdout. write("💬 Seeding comments...")
        comment_data = [
            (t5, manager, "Looks solid, I'll review the reset flow tomorrow. "),
            (t6, qa, "Tested on IE11 - fixed!  Styles look good now."),
            (t8, dev1, "Can we align on scopes? Need to clarify which AD tenant. "),
            (crm2, manager, "High priority - blocking pilot.  Please investigate asap."),
            (crm3, client, "This is crucial for our sales team.  Great idea!"),
            (lp1, dev2, "Almost done with the modal, waiting on design specs."),
            (c_t1, dev1, "✅ Completed successfully"),
            (c_t2, dev2, "✅ All tests passing"),
        ]

        for task, user, text in comment_data:
            comment = Comment(content=text, author=user)
            comment_repo.save(comment, task. get_id())
            self.stdout.write(f"  ✓ Comment on {task.get_title()[: 30]}")

        # === SUCCESS ===
        self.stdout.write(self.style.SUCCESS("\n=== ✅ [Seed Complete! ] ===\n"))
        print("\n" + "="*60)
        print("🔐 DEMO CREDENTIALS:")
        print("="*60)
        print("Admin:        root        / demo123")
        print("Manager:      manager1    / demo123")
        print("Developer:    dev1        / demo123")
        print("Developer:   dev2        / demo123")
        print("QA:          qa1         / demo123")
        print("Client:      client1     / demo123")
        print("="*60)
        print("\n CREATED:")
        print("  • 6 Users (all roles)")
        print("  • 3 Projects")
        print("  • 4 Sprints (1 completed, 3 active)")
        print("  • 14 Tasks total:")
        print("    - 4 DONE (completed sprint - Team Velocity)")
        print("    - 5 In Progress (current workload)")
        print("    - 5 To Do (backlog)")
        print("  • 7 Tags")
        print("  • 8 Comments")
        print("\n🎯 READY FOR DEMO!")
        print("="*60)