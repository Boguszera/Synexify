# domain/projects/internal_project.py
from .project_base import ProjectBase

class InternalProject(ProjectBase):
    def archive(self):
        self._archived = True

    def is_archived(self) -> bool:
        return getattr(self, "_archived", False)