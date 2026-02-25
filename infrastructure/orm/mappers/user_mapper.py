# infrastructure/orm/mappers/user_mapper.py

from domain.users.user_base import UserBase
from infrastructure.orm.models.user_model import UserModel


class UserMapper:
    @staticmethod
    def to_domain(model: UserModel) -> UserBase:
        # UserBase __init__(name, email, role, login, user_id: Optional[str] = None)
        user = UserBase(name=model.name, email=model.email, role=model.role, login=model.login, user_id=str(model.id))
        return user

    @staticmethod
    def to_orm(user: UserBase, model: UserModel | None = None) -> UserModel:
        if model is None:
            model = UserModel(id=user.get_id())
        model.name = user.get_name()
        model.email = user.get_email()
        model.role = user.get_role()
        model.login = user.get_login()
        return model
