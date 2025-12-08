# application/admin_panel_service.py
from domain.users.user_base import UserBase
from domain.projects.project_base import ProjectBase

class AdminPanelService:
    def __init__(self, auth_service, user_repo, project_repo):
        self.auth_service = auth_service
        self.user_repo = user_repo
        self.project_repo = project_repo

    # ---- Users ----
    def list_users(self, filters=None, user: UserBase = None):
        self.auth_service.check_manage_user(user, user)
        users = self.user_repo.list_all()
        return users

    def create_user(self, name, email, role, login, user: UserBase):
        self.auth_service.check_manage_user(user, user)
        new_user = UserBase(name=name, email=email, role=role, login=login)
        self.user_repo.save(new_user)
        return new_user

    def update_user(self, user_id: str, fields: dict, user: UserBase):
        target_user = self.get_user_by_id(user_id)
        if not target_user:
            raise ValueError("User not found")
        self.auth_service.check_manage_user(user, target_user)
        allowed_fields = {"name", "email", "role", "login"}
        for k, v in fields.items():
            if k in allowed_fields:
                setattr(target_user, f"_{k}", v)
        self.user_repo.save(target_user)
        return target_user

    def delete_user(self, user_id: str, user: UserBase):
        target_user = self.get_user_by_id(user_id)
        if not target_user:
            raise ValueError("User not found")
        self.auth_service.check_manage_user(user, target_user)
        self.user_repo.delete(target_user.get_id())

    def get_user_by_id(self, user_id: str):
        user = self.user_repo.get_by_id(user_id)
        return user

    # ---- Projects ----
    def list_projects(self, filters=None, user: UserBase = None):
        self.auth_service.check_manage_user(user, user)
        projects = self.project_repo.list_all()
        return projects

    def create_project(self, name, description, manager=None, user: UserBase = None):
        self.auth_service.check_manage_user(user, user)
        project = ProjectBase(name=name, description=description)
        if manager:
            project.add_member_id(manager.get_id())
        self.project_repo.save(project)
        return project

    def update_project(self, project: ProjectBase, fields: dict, user: UserBase):
        self.auth_service.check_manage_user(user, user)
        for k, v in fields.items():
            setattr(project, k, v)
        self.project_repo.save(project)

    def delete_project(self, project: ProjectBase, user: UserBase):
        self.auth_service.check_manage_user(user, user)
        self.project_repo.delete(project.get_id())
