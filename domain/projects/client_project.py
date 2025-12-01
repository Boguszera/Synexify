# domain/projects/client_project.py
from .project_base import ProjectBase
from typing import Dict

class ClientProject(ProjectBase):
    def get_report_data(self) -> Dict:
        data = super().get_report_data()
        data["members"] = None  # the customer cannot see the list of members
        return data