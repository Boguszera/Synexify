# application/authorization_service.py

from domain.exceptions.exceptions import PermissionDenied
from domain.users.admin_user import AdminUser
from domain.users.manager_user import ManagerUser
from domain.users.team_member_user import  TeamMemberUser
from domain.users.client_user import ClientUser
from domain.users.user_base import UserBase

class AuthorizationService:

    def can_edit_task(self, user: UserBase, task) -> bool:
        if isinstance(user, AdminUser) or isinstance(user, ManagerUser):
            return True
        return False

    def can_assign_task(self, user: UserBase, task) -> bool:
        return isinstance(user, (AdminUser, ManagerUser))

    def can_view_project(self, user: UserBase, project) -> bool:
        if isinstance(user, AdminUser):
            return True
        if isinstance(user, (ManagerUser, TeamMemberUser, ClientUser)):
            return user.get_id() in project.get_member_ids()
        return False

    def can_manage_user(self, user: UserBase, target_user: UserBase) -> bool:
        return isinstance(user, AdminUser)

    def can_manage_project(self, user: UserBase, project) -> bool:
        if isinstance(user, AdminUser):
            return True
        if isinstance(user, ManagerUser):
            return user.get_id() in project.get_member_ids()
        return False

    def check_manage_project(self, user, project):
        if project is None:
            raise PermissionDenied(user.get_id(), action="manage_project", resource="Project is None")
        if not self.can_manage_project(user, project):
            raise PermissionDenied(user.get_id(), action="manage_project", resource=project.get_id())

    def check_view_project(self, user, project):
        if not self.can_view_project(user, project):
            raise PermissionDenied(user.get_id(), action="view_project", resource=project.get_id())

    def check_manage_user(self, user, target_user):
        if not self.can_manage_user(user, target_user):
            raise PermissionDenied(user.get_id(), action="manage_user", resource=target_user.get_id())
