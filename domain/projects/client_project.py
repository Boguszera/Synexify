# domain/projects/client_project.py

from .project_base import ProjectBase


class ClientProject(ProjectBase):
    def get_report_data(self, task_loader_callable=None) -> dict:
        data = super().get_report_data(task_loader_callable)
        data["members"] = None  # customers does not see team members
        return data
