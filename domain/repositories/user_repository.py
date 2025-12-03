from abc import ABC, abstractmethod
from typing import Optional, List
from domain.users.user_base import UserBase

class UserRepository(ABC):
    @abstractmethod
    def get_by_id(self, user_id: str) -> Optional[UserBase]:
        pass

    @abstractmethod
    def get_by_login(self, login: str) -> Optional[UserBase]:
        pass

    @abstractmethod
    def save(self, user: UserBase) -> None:
        pass

    @abstractmethod
    def delete(self, user_id: int) -> None:
        pass

    @abstractmethod
    def list_all(self) -> List[UserBase]:
        pass
