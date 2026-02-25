from abc import ABC, abstractmethod

from domain.users.user_base import UserBase


class UserRepository(ABC):
    @abstractmethod
    def get_by_id(self, user_id: str) -> UserBase | None:
        pass

    @abstractmethod
    def get_by_login(self, login: str) -> UserBase | None:
        pass

    @abstractmethod
    def save(self, user: UserBase) -> None:
        pass

    @abstractmethod
    def delete(self, user_id: int) -> None:
        pass

    @abstractmethod
    def list_all(self) -> list[UserBase]:
        pass
