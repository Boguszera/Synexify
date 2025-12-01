class AdminPanelService:
    def __init__(self, auth_service):
        self.auth_service = auth_service

    def list_users(self, filters=None, user=None):
        self.auth_service.check_manage_user(user, user)
        # repo/persistence
        pass

    def create_user(self, name, email, role, login, user):
        self.auth_service.check_manage_user(user, user)
        pass

    def update_user(self, target_user, fields, user):
        self.auth_service.check_manage_user(user, target_user)
        pass

    def delete_user(self, target_user, user):
        self.auth_service.check_manage_user(user, target_user)
        pass

    def list_projects(self, filters=None, user=None):
        self.auth_service.check_manage_user(user, user)
        pass

    def create_project(self, name, description, manager=None, user=None):
        self.auth_service.check_manage_user(user, user)
        pass

    def update_project(self, project, fields, user):
        self.auth_service.check_manage_user(user, user)
        pass

    def delete_project(self, project, user):
        self.auth_service.check_manage_user(user, user)
        pass
