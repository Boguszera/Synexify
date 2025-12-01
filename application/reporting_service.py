# application/reporting_service.py
from datetime import datetime
from domain.users.user_base import UserBase
from domain.projects.project_base import ProjectBase

class ReportingService:
    def __init__(self, auth_service, task_repo):
        self.auth_service = auth_service
        self.task_repo = task_repo

    def team_workload(self, project: ProjectBase, user: UserBase) -> dict:
        self.auth_service.check_manage_project(user, project)
        workload = {}
        for member_id in project.get_member_ids():
            tasks_for_member = [
                task for task_id in project.get_task_ids()
                if (task := self.task_repo.get(task_id))
                and member_id in task.get_assignees_ids()
            ]
            workload[member_id] = len(tasks_for_member)
        return workload

    def project_progress(self, project: ProjectBase, user: UserBase) -> dict:
        self.auth_service.check_view_project(user, project)
        total_tasks = len(project.get_task_ids())
        tasks_done = 0
        for task_id in project.get_task_ids():
            task = self.task_repo.get(task_id)
            if task and task.get_status().lower() == "done":
                tasks_done += 1
        completion_percentage = (tasks_done / total_tasks * 100) if total_tasks else 0
        return {
            "completion_percentage": completion_percentage,
            "total_tasks": total_tasks,
            "tasks_done": tasks_done
        }

    def deadline_report(self, project: ProjectBase, user: UserBase) -> dict:
        self.auth_service.check_manage_project(user, project)
        now = datetime.now()
        overdue_tasks = []
        for task_id in project.get_task_ids():
            task = self.task_repo.get(task_id)
            if not task:
                continue
            due_date = task.get_due_date()
            if due_date and due_date < now and task.get_status().lower() != "done":
                overdue_tasks.append(task)
        avg_delay = sum((now - t.get_due_date()).days for t in overdue_tasks) / len(overdue_tasks) if overdue_tasks else 0
        return {
            "overdue_count": len(overdue_tasks),
            "average_delay_days": avg_delay
        }

    def dashboard_overview(self, user: UserBase, projects: list[ProjectBase]) -> list[dict]:
        overview = []
        for project in projects:
            if not self.auth_service.can_view_project(user, project):
                continue
            member_task_counts = {}
            for member_id in project.get_member_ids():
                tasks_for_member = [
                    task for task_id in project.get_task_ids()
                    if (task := self.task_repo.get(task_id))
                    and member_id in task.get_assignees_ids()
                ]
                member_task_counts[member_id] = len(tasks_for_member)

            progress = self.project_progress(project, user)
            overview.append({
                "project": project,
                "progress": progress,
                "members_task_counts": member_task_counts
            })
        return overview
