from django.db import transaction
from domain.repositories.user_repository import UserRepository
from domain.users.user_base import UserBase

from infrastructure.orm.models.user_model import UserModel
from infrastructure.orm.mappers.user_mapper import UserMapper


class UserDjangoRepository(UserRepository):

    def get_by_id(self, user_id: str) -> UserBase | None:
        model = UserModel.objects.filter(id=user_id).first()
        if not model:
            return None
        return UserMapper.to_domain(model)

    def get_by_login(self, login: str) -> UserBase | None:
        model = UserModel.objects.filter(login=login).first()
        if not model:
            return None
        return UserMapper.to_domain(model)

    def list_all(self) -> list[UserBase]:
        return [UserMapper.to_domain(u) for u in UserModel.objects.all()]

    def save(self, user: UserBase) -> UserBase:
        with transaction.atomic():
            model = UserModel.objects.filter(id=user.get_id()).first()
            model = UserMapper.to_orm(user, model)
            model.save()
        return UserMapper.to_domain(model)

    def delete(self, user_id: str) -> None:
        UserModel.objects.filter(id=user_id).delete()
