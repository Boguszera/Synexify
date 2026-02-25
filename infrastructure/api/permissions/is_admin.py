# infrastructure/api/permissions/is_admin.py
from rest_framework.permissions import BasePermission

from infrastructure.adapters.user_adapter import to_domain_user


class IsAdmin(BasePermission):
    def has_permission(self, request, view):
        domain_user = to_domain_user(request.user)
        return domain_user and domain_user.get_role() == "admin"
