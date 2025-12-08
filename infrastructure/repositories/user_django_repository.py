# infrastructure/repositories/user_django_repository.py
from infrastructure.orm.models.user_model import UserModel
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

class UserDjangoRepository:

    def _to_domain(self, orm_obj):
        cls = ROLE_CLASS_MAP.get(orm_obj.role)
        if not cls:
            raise ValueError(f"Unknown role: {orm_obj.role}")
        return cls(
            user_id=str(orm_obj.id),
            name=orm_obj.name,
            email=orm_obj.email,
            role=orm_obj.role,
            login=orm_obj.login
        )

    def get_by_login(self, login):
        try:
            user = UserModel.objects.get(login=login)
            return self._to_domain(user)
        except UserModel.DoesNotExist:
            return None

    def get_by_id(self, user_id):
        try:
            user = UserModel.objects.get(id=user_id)
            return self._to_domain(user)
        except UserModel.DoesNotExist:
            return None

    def list_all(self):
        return [self._to_domain(u) for u in UserModel.objects.all()]

    def save(self, domain_user, password=None):
        try:
            user = UserModel.objects.get(login=domain_user.get_login())
            user.name = domain_user.get_name()
            user.email = domain_user.get_email()
            user.role = domain_user.get_role()
            if password:
                user.set_password(password)
            user.save()
        except UserModel.DoesNotExist:
            user = UserModel.objects.create_user(
                login=domain_user.get_login(),
                email=domain_user.get_email(),
                name=domain_user.get_name(),
                role=domain_user.get_role(),
                password=password or "test123"
            )
        return self._to_domain(user)

    def delete(self, user_id: str):
        UserModel.objects.filter(id=user_id).delete()
