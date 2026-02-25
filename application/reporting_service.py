# application/reporting_service.py
from datetime import datetime

from domain.projects.project_base import ProjectBase
from domain.tasks.feature_task import FeatureTask
from domain.users.user_base import UserBase


class ReportingService:
    def __init__(self, auth_service, task_repo, project_repo, user_repo):
        self.auth_service = auth_service
        self.task_repo = task_repo
        self.project_repo = project_repo
        self.user_repo = user_repo

    def get_task_status_summary_all(self, user: UserBase) -> dict[str, int]:
        all_tasks = self.task_repo.get_all()
        status_counts = {"To Do": 0, "In Progress": 0, "Done": 0, "Blocked": 0}

        for task in all_tasks:
            project = self.project_repo.get_by_id(task.get_project_id())
            if not project or not self.auth_service.can_view_project(user, project):
                continue

            status = task.get_status()
            if status in status_counts:
                status_counts[status] += 1
            elif status:
                status_counts[status] = status_counts.get(status, 0) + 1

        return status_counts

    def get_team_workload_summary(
        self, user: UserBase, project_id: str = None
    ) -> list[dict[str, str | int | UserBase]]:
        all_tasks = self.task_repo.get_all()

        workload_map = {}

        for task in all_tasks:
            if project_id and task.get_project_id() != project_id:
                continue
            project = self.project_repo.get_by_id(task.get_project_id())
            if not project or not self.auth_service.can_view_project(user, project):
                continue

            if task.get_status() == "Done":
                continue

            points = task.get_story_points() if isinstance(task, FeatureTask) else 0

            for assignee_id in task.get_assignees_ids():
                if assignee_id not in workload_map:
                    workload_map[assignee_id] = {"tasks_count": 0, "points_sum": 0}

                workload_map[assignee_id]["tasks_count"] += 1
                workload_map[assignee_id]["points_sum"] += points

        result = []
        for user_id, data in workload_map.items():
            member = self.user_repo.get_by_id(user_id)
            if member:
                result.append(
                    {
                        "user": member,
                        "tasks_count": data["tasks_count"],
                        "points_sum": data["points_sum"],
                    }
                )

        return sorted(result, key=lambda x: (x["points_sum"], x["tasks_count"]), reverse=True)

    def team_workload_by_project(self, project: ProjectBase, user: UserBase) -> dict:
        self.auth_service.check_manage_project(user, project)
        workload = {}
        for member_id in project.get_member_ids():
            tasks_for_member = [
                task
                for task_id in project.get_task_ids()
                if (task := self.task_repo.get(task_id)) and member_id in task.get_assignees_ids()
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
        return {"completion_percentage": completion_percentage, "total_tasks": total_tasks, "tasks_done": tasks_done}

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
        avg_delay = (
            sum((now - t.get_due_date()).days for t in overdue_tasks) / len(overdue_tasks) if overdue_tasks else 0
        )
        return {"overdue_count": len(overdue_tasks), "average_delay_days": avg_delay}

    def dashboard_overview(self, user: UserBase, projects: list[ProjectBase]) -> list[dict]:
        overview = []
        for project in projects:
            if not self.auth_service.can_view_project(user, project):
                continue
            member_task_counts = {}
            for member_id in project.get_member_ids():
                tasks_for_member = [
                    task
                    for task_id in project.get_task_ids()
                    if (task := self.task_repo.get(task_id)) and member_id in task.get_assignees_ids()
                ]
                member_task_counts[member_id] = len(tasks_for_member)

            progress = self.project_progress(project, user)
            overview.append({"project": project, "progress": progress, "members_task_counts": member_task_counts})
        return overview
