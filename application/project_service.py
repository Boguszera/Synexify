# application/project_service.py

from domain.projects.project_base import ProjectBase
from domain.exceptions.exceptions import PermissionDenied

class ProjectService:
    def __init__(self, auth_service, project_repo):
        self.auth = auth_service
        self.project_repo = project_repo

    # ---- CRUD Projects ----
    def list_projects(self, user):
        all_projects = self.project_repo.list_all()
        visible_projects = [
            p for p in all_projects
            if self.auth.can_view_project(user, p)
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
        if "name" in fields:
            project.set_name(fields["name"])
        if "description" in fields:
            project.set_description(fields["description"])
        if "archived" in fields:
            project.set_archived(fields["archived"])

        return self.project_repo.save(project)

    def delete_project(self, project: ProjectBase, user):
        self.auth.check_manage_project(user, project)
        self.project_repo.delete(project.get_id())

