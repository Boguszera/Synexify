# infrastructure/adapters/user_adapter.py
from domain.users.admin_user import AdminUser
from domain.users.manager_user import ManagerUser
from domain.users.team_member_user import TeamMemberUser
from domain.users.client_user import ClientUser

def to_domain_user(django_user):
    role = getattr(django_user, 'role', 'team_member')
    if role == 'admin':
        return AdminUser(name=django_user.username, email=django_user.email, role=role, login=django_user.username)
    elif role == 'manager':
        return ManagerUser(name=django_user.username, email=django_user.email, role=role, login=django_user.username)
    elif role == 'client':
        return ClientUser(name=django_user.username, email=django_user.email, role=role, login=django_user.username)
    else:
        return TeamMemberUser(name=django_user.username, email=django_user.email, role=role, login=django_user.username)
