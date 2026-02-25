# infrastructure/api/permissions/sprint_permissions.py


class SprintPermissions:
    @staticmethod
    def can_view(user, sprint, project):
        if user.get_role() == "admin":
            return True
        if user.get_role() in ("manager", "team_member") and user.get_id() in project.get_member_ids():
            return True
        return False

    @staticmethod
    def can_edit(user, sprint, project):
        if user.get_role() == "admin":
            return True
        if user.get_role() == "manager" and user.get_id() in project.get_member_ids():
            return True
        return False

    @staticmethod
    def can_delete(user, sprint, project):
        return SprintPermissions.can_edit(user, sprint, project)

    @staticmethod
    def can_create(user, project):
        if user.get_role() == "admin":
            return True
        if user.get_role() == "manager" and user.get_id() in project.get_member_ids():
            return True
        return False
