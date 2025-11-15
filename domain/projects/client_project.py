# domain/projects/client_project.py
from .project_base import ProjectBase

class ClientProject(ProjectBase):
    def generate_report(self):
        return f"Client Project {self._name}: limited report"