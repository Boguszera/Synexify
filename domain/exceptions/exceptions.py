# domain/exceptions/exceptions.py

class DomainError(Exception):
    pass

class PermissionDenied(DomainError):
    pass

class InvalidOperationError(DomainError):
    pass

class TaskStatusTransitionError(DomainError):
    pass

class NotFoundError(DomainError):
    pass
