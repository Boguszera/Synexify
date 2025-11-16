# domain/users/admin_user.py
from .user_base import UserBase

class AdminUser(UserBase):
    def manage_users(self):
        pass  # app service

    def manage_projects(self):
        pass  # app service