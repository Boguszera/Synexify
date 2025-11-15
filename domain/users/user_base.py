# domain/users/user_base.py
class UserBase:
    def __init__(self, user_id, name, email, role, login):
        self._id = user_id
        self._name = name
        self._email = email
        self._role = role
        self._login = login
        self._tasks = []

    def get_tasks(self):
        return self._tasks

    def get_role(self):
        return self._role

    def set_role(self, role):
        self._role = role

    def add_comment(self, task, content):
        task.add_comment({'author': self, 'content': content})