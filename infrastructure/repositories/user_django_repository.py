# infrastructure/repositories/user_django_repository.py
from infrastructure.orm.models.user_model import UserModel
from infrastructure.adapters.user_adapter import to_domain_user

class UserDjangoRepository:

    def _to_domain(self, orm_obj):
        return to_domain_user(orm_obj)

    def get_by_login(self, login):
        try:
            return self._to_domain(UserModel.objects.get(login=login))
        except UserModel.DoesNotExist:
            return None

    def get_by_id(self, user_id):
        try:
            return self._to_domain(UserModel.objects.get(id=user_id))
        except UserModel.DoesNotExist:
            return None

    def list_all(self):
        return [self._to_domain(u) for u in UserModel.objects.all()]

    def save(self, domain_user, password=None):

        orm_user, created = UserModel.objects.update_or_create(
            id=domain_user.get_id(),
            defaults={
                "login": domain_user.get_login(),
                "email": domain_user.get_email(),
                "name": domain_user.get_name(),
                "role": domain_user.get_role(),
            }
        )

        if password:
            orm_user.set_password(password)
            orm_user.save()

        return self._to_domain(orm_user)

    def delete(self, user_id: str):
        UserModel.objects.filter(id=user_id).delete()