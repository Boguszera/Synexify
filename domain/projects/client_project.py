# domain/projects/client_project.py
from .project_base import ProjectBase

class ClientProject(ProjectBase):
    def generate_report(self) -> str:
        return f"Client Project '{self.get_name()}': {len(self.get_tasks())} tasks, {len(self.get_members())} members (limited view)"
