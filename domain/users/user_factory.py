# domain/users/user_factory.py

from .admin_user import AdminUser
from .manager_user import ManagerUser
from .team_member_user import TeamMemberUser
from .client_user import ClientUser

ROLE_MAP = {
    "admin": AdminUser,
    "manager": ManagerUser,
    "team_member": TeamMemberUser,
    "client": ClientUser,
}

class UserFactory:
    @staticmethod
    def create(name, email, role, login):
        cls = ROLE_MAP.get(role)
        if not cls:
            raise ValueError(f"Unknown role: {role}")

        return cls(
            name=name,
            email=email,
            role=role,
            login=login
        )
