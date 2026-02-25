from infrastructure.adapters.user_adapter import to_domain_user
from infrastructure.di import Container


def get_container():
    return Container()


def get_domain_user(request):
    """Django (request.user) -> Domain user."""
    if not request.user.is_authenticated:
        return None
    return to_domain_user(request.user)
