# infrastructure/api/permissions/project_permissions.py


class ProjectPermissions:
    @staticmethod
    def can_view(user, project):
        if user.get_role() == "admin":
            return True
        if user.get_role() in ("manager", "team_member") and user.get_id() in project.get_member_ids():
            return True
        return False

    @staticmethod
    def can_edit(user, project):
        if user.get_role() == "admin":
            return True
        if user.get_role() == "manager" and user.get_id() in project.get_member_ids():
            return True
        return False

    @staticmethod
    def can_delete(user, project):
        if user.get_role() == "admin":
            return True
        if user.get_role() == "manager" and user.get_id() in project.get_member_ids():
            return True
        return False

    @staticmethod
    def can_create(user):
        return user.get_role() in ["admin", "manager"]
