from datetime import datetime
from domain.exceptions.exceptions import PermissionDenied
from domain.interfaces.reportable import Reportable
from domain.users.user_base import UserBase
from domain.projects.project_base import ProjectBase


class ReportingService:
    def __init__(self, auth_service):
        self.auth_service = auth_service

    def team_workload(self, project: ProjectBase, user: UserBase) -> dict:
        """
        Counts the number of tasks assigned to each project member.
        Permissions: admin or manager.
        """
        self.auth_service.check_manage_project(user, project)
        workload = {}
        for member in project.get_members():
            workload[member.get_id()] = sum(
                1 for task in project.get_all_tasks() if member in task.get_assignees()
            )
        return workload

    def project_progress(self, project: ProjectBase, user: UserBase) -> dict:
        """
        Calculates the % of project completion and the number of tasks in each status.
        Permissions: any user who can view the project.
        """
        self.auth_service.check_view_project(user, project)
        all_tasks = project.get_all_tasks()
        done_tasks = [t for t in all_tasks if t.get_status().lower() == "done"]
        completion = (len(done_tasks) / len(all_tasks) * 100) if all_tasks else 0
        return {
            "completion_percentage": completion,
            "total_tasks": len(all_tasks),
            "tasks_done": len(done_tasks)
        }

    def deadline_report(self, project: ProjectBase, user: UserBase) -> dict:
        """
        Report on exceeded tasks and average delay.
        Permissions: admin or manager.
        """
        self.auth_service.check_manage_project(user, project)
        now = datetime.now()
        overdue_tasks = [
            t for t in project.get_all_tasks()
            if t.get_due_date() and t.get_due_date() < now and t.get_status().lower() != "done"
        ]
        avg_delay = (
            sum((now - t.get_due_date()).days for t in overdue_tasks) / len(overdue_tasks)
            if overdue_tasks else 0
        )
        return {
            "overdue_count": len(overdue_tasks),
            "average_delay_days": avg_delay
        }

    def dashboard_overview(self, user: UserBase, projects: list[ProjectBase]) -> list[dict]:
        """
        Dashboard showing a list of user projects along with progress
        and team member workload.
        Permissions: every project that the user can see.
        """
        overview = []
        for project in projects:
            if not self.auth_service.can_view_project(user, project):
                continue
            progress = self.project_progress(project, user)
            members = project.get_members()
            member_task_counts = {
                m.get_id(): len([t for t in project.get_all_tasks() if m in t.get_assignees()])
                for m in members
            }
            overview.append({
                "project": project,
                "progress": progress,
                "members_task_counts": member_task_counts
            })
        return overview
