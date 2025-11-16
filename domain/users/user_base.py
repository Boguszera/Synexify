# domain/users/user_base.py
class UserBase:
    VALID_ROLES = {"admin", "manager", "team_member", "client"}

    def __init__(self, user_id: int, name: str, email: str, role: str, login: str):
        self._id = user_id
        self._name = name
        self._email = email
        # self._role = role
        self._login = login
        # self._tasks = []

        if role not in self.VALID_ROLES:
            raise ValueError(f"Invalid role '{role}', must be one of: {', '.join(self.VALID_ROLES)}")
        self._role = role

    def get_id(self):
        return self._id

    def get_name(self):
        return self._name

    def get_email(self):
        return self._email

    def get_role(self):
        return self._role

    def get_login(self):
        return self._login

    """
    def get_tasks(self):
        return self._tasks 
    """

    def set_role(self, role: str):
        if role not in self.VALID_ROLES:
            raise ValueError(f"Invalid role '{role}', must be one of: {', '.join(self.VALID_ROLES)}")
        self._role = role

    def add_comment(self, task, content: str):
        # creates a domain comment object. persistence layer is responsible for saving it.
        from domain.comments.comment import Comment
        from domain.interfaces.commentable import Commentable

        if not isinstance(task, Commentable):
            raise TypeError("task must implement Commentable interface")

        if not isinstance(content, str) or not content.strip():
            raise ValueError("Comment content cannot be empty")

        comment = Comment(content=content, author=self)
        task.add_comment(comment)