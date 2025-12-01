# domain/users/user_base.py
class UserBase:
    VALID_ROLES = {"admin", "manager", "team_member", "client"}

    def __init__(self, user_id: int, name: str, email: str, role: str, login: str):
        if role not in self.VALID_ROLES:
            raise ValueError(f"Invalid role '{role}'")
        self._id = user_id
        self._name = name
        self._email = email
        self._login = login
        self._role = role

    def get_id(self) -> int:
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