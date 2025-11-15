# domain/users/admin_user.py
from .user_base import UserBase

class AdminUser(UserBase):
    def manage_users(self):
        pass  # CRUD users

    def manage_projects(self):
        pass  # CRUD projects