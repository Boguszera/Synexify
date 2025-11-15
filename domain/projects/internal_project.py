# domain/projects/internal_project.py
from .project_base import ProjectBase

class InternalProject(ProjectBase):
    def archive(self):
        self._archived = True