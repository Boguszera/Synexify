from datetime import datetime
from domain.exceptions.exceptions import PermissionDenied
from domain.interfaces.reportable import Reportable
from domain.users.user_base import UserBase
from domain.projects.project_base import ProjectBase


class ReportingService:
    def __init__(self, auth_service):
        self.auth_service = auth_service

    def team_workload(self, project: ProjectBase, user: UserBase) -> dict:
        """Counts the number of tasks assigned to each project member."""
        self.auth_service.check_manage_project(user, project)
        report_data = project.get_report_data()
        workload = {}
        for member in report_data.get("members", []):
            workload[member.get_id()] = sum(
                1 for task in project.get_all_tasks() if member in task.get_assignees()
            )
        return workload

    def project_progress(self, project: ProjectBase, user: UserBase) -> dict:
        """Returns project completion percentage and tasks done."""
        self.auth_service.check_view_project(user, project)
        report_data = project.get_report_data()
        return {
            "completion_percentage": report_data["completion_percentage"],
            "total_tasks": report_data["total_tasks"],
            "tasks_done": report_data["tasks_done"]
        }

    def deadline_report(self, project: ProjectBase, user: UserBase) -> dict:
        """Report on overdue tasks and average delay."""
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
        """Returns dashboard overview for user projects."""
        overview = []
        for project in projects:
            if not self.auth_service.can_view_project(user, project):
                continue
            report_data = project.get_report_data()
            member_task_counts = {
                m.get_id(): len([t for t in project.get_all_tasks() if m in t.get_assignees()])
                for m in report_data.get("members", [])
            }
            overview.append({
                "project": project,
                "progress": {
                    "completion_percentage": report_data["completion_percentage"],
                    "total_tasks": report_data["total_tasks"],
                    "tasks_done": report_data["tasks_done"]
                },
                "members_task_counts": member_task_counts
            })
        return overview