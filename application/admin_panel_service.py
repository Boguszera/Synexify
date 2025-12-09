# application/admin_panel_service.py
from domain.users.user_factory import UserFactory
from domain.users.user_base import UserBase

class AdminPanelService:
    def __init__(self, auth_service, user_repo, project_repo):
        self.auth_service = auth_service
        self.user_repo = user_repo
        self.project_repo = project_repo

    # ---- Users ----
    def list_users(self, filters=None, user: UserBase = None):
        self.auth_service.check_manage_user(user, user)
        return self.user_repo.list_all()

    def create_user(self, name, email, role, login, password, user: UserBase):
        self.auth_service.check_manage_user(user, user)

        new_user = UserFactory.create(
            name=name,
            email=email,
            role=role,
            login=login
        )

        saved = self.user_repo.save(new_user, password=password)
        return saved

    def update_user(self, user_id: str, fields: dict, user: UserBase):
        target_user = self.get_user_by_id(user_id)
        if not target_user:
            raise ValueError("User not found")

        self.auth_service.check_manage_user(user, target_user)

        allowed_fields = {"name", "email", "role", "login"}
        for k, v in fields.items():
            if k in allowed_fields:
                setattr(target_user, f"_{k}", v)

        return self.user_repo.save(target_user)

    def delete_user(self, user_id: str, user: UserBase):
        target_user = self.get_user_by_id(user_id)
        if not target_user:
            raise ValueError("User not found")

        self.auth_service.check_manage_user(user, target_user)
        self.user_repo.delete(target_user.get_id())

    def get_user_by_id(self, user_id: str):
        return self.user_repo.get_by_id(user_id)
