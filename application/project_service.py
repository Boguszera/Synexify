# application/project_service.py

from domain.projects.project_base import ProjectBase
from domain.exceptions.exceptions import PermissionDenied
from infrastructure.api.permissions.project_permissions import ProjectPermissions

class ProjectService:
    def __init__(self, auth_service, project_repo):
        self.auth = auth_service
        self.project_repo = project_repo

    # ---- CRUD Projects ----
    def list_projects(self, user):
        all_projects = self.project_repo.list_all()
        visible_projects = [
            p for p in all_projects if self.can_view(user, p)
        ]
        return visible_projects

    def create_project(self, name: str, description: str, user):
        from domain.projects.project_base import ProjectBase
        from infrastructure.api.permissions.project_permissions import ProjectPermissions
        from domain.exceptions.exceptions import PermissionDenied

        if not ProjectPermissions.can_create(user):
            raise PermissionDenied("You do not have permission to create a project")

        project = ProjectBase(name=name, description=description)
        project.add_member_id(user.get_id())
        project.add_manager_id(user.get_id())
        saved_project = self.project_repo.save(project)

        return saved_project

    def get_project(self, project_id: str):
        return self.project_repo.get_by_id(project_id)

    def update_project(self, project: ProjectBase, fields: dict, user):
        self.auth.check_manage_project(user, project)
        allowed_fields = {"name", "description", "archived"}
        for k, v in fields.items():
            if k in allowed_fields:
                setattr(project, f"_{k}", v)
        return self.project_repo.save(project)

    def delete_project(self, project: ProjectBase, user):
        self.auth.check_manage_project(user, project)
        self.project_repo.delete(project.get_id())

    # ---- Permissions helper ----
    def can_view(self, user, project):
        role = user.get_role()
        if role == "admin":
            return True
        if role == "manager" or role == "team_member":
            return user.get_id() in project.get_member_ids()
        return False
