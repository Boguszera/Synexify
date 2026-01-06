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

    def set_name(self, name: str):
        if not name or not name.strip():
            raise ValueError("Name cannot be empty")
        self._name = name.strip()

    def set_email(self, email: str):
        if not email or "@" not in email:
            raise ValueError("Invalid email format")
        self._email = email.lower().strip()

    def set_role(self, role: str):
        if role not in self.VALID_ROLES:
            raise ValueError(f"Invalid role '{role}'")
        self._role = role

    def set_login(self, login: str):
        if not login or not login.strip():
            raise ValueError("Login cannot be empty")
        if len(login) < 3:
            raise ValueError("Login must be at least 3 characters")
        self._login = login.strip()