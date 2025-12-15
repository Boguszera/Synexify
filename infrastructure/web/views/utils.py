from infrastructure.di import Container
from infrastructure.adapters.user_adapter import to_domain_user

def get_container():
    """Zwraca nową instancję kontenera DI."""
    return Container()

def get_domain_user(request):
    """Konwertuje użytkownika Django (z request.user) na użytkownika Domenowego."""
    if not request.user.is_authenticated:
        return None
    return to_domain_user(request.user)