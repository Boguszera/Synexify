# domain/exceptions/exceptions.py

class DomainError(Exception):
    pass

class PermissionDenied(DomainError):
    def __init__(self, user_id: str, action: str, resource: str = None):
        self.user_id = user_id
        self.action = action
        self.resource = resource
        super().__init__(f"PermissionDenied: user={user_id}, action={action}, resource={resource}")

class InvalidOperationError(DomainError):
    pass

class TaskStatusTransitionError(DomainError):
    pass

class NotFoundError(DomainError):
    pass
