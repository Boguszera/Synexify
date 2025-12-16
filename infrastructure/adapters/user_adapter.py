# infrastructure/adapters/user_adapter.py

from domain.users.admin_user import AdminUser
from domain.users.manager_user import ManagerUser
from domain.users.team_member_user import TeamMemberUser
from domain.users.client_user import ClientUser

ROLE_CLASS_MAP = {
    "admin": AdminUser,
    "manager": ManagerUser,
    "team_member": TeamMemberUser,
    "client": ClientUser,
}

from domain.users.admin_user import AdminUser
from domain.users.manager_user import ManagerUser
from domain.users.team_member_user import TeamMemberUser
from domain.users.client_user import ClientUser

ROLE_CLASS_MAP = {
    "admin": AdminUser,
    "manager": ManagerUser,
    "team_member": TeamMemberUser,
    "client": ClientUser,
}

def to_domain_user(user_model):
    role = getattr(user_model, 'role', 'team_member')
    cls = ROLE_CLASS_MAP.get(role)

    if not cls:
        raise ValueError(f"Unknown role: {role}")
    display_name = user_model.name
    if not display_name:
        display_name = user_model.login
    if not display_name:
        display_name = user_model.email
    if not display_name:
        display_name = "Unknown User"

    return cls(
        user_id=str(user_model.id),
        name=display_name,
        email=user_model.email,
        role=role,
        login=user_model.login,
    )

def to_dict(domain_user):
    return {
        "id": domain_user.get_id(),
        "login": domain_user.get_login(),
        "name": domain_user.get_name(),
        "email": domain_user.get_email(),
        "role": domain_user.get_role(),
    }
