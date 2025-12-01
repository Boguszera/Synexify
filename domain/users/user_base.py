# domain/users/user_base.py
import uuid
from typing import Optional

class UserBase:
    VALID_ROLES = {"admin", "manager", "team_member", "client"}

    def __init__(self, name: str, email: str, role: str, login: str, user_id: Optional[str] = None):
        if role not in self.VALID_ROLES:
            raise ValueError(f"Invalid role '{role}'")
        self._id = user_id or str(uuid.uuid4())
        self._name = name
        self._email = email
        self._role = role
        self._login = login

    def get_id(self) -> str:
        return self._id

    def get_name(self) -> str:
        return self._name

    def get_email(self) -> str:
        return self._email

    def get_role(self) -> str:
        return self._role

    def get_login(self) -> str:
        return self._login

    def set_role(self, role: str):
        if role not in self.VALID_ROLES:
            raise ValueError(f"Invalid role '{role}'")
        self._role = role