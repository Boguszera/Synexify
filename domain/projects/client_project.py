# domain/projects/client_project.py
from .project_base import ProjectBase
from typing import Dict

class ClientProject(ProjectBase):
    def get_report_data(self, task_loader_callable=None) -> Dict:
        data = super().get_report_data(task_loader_callable)
        data["members"] = None  # customers does not see team members
        return data
