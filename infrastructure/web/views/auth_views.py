# infrastructure/web/views/auth_views.py

from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages


def login_view(request):
    """
    Obsługuje logowanie sesyjne dla frontendu MTV.
    Używa Twojego niestandardowego backendu (pole 'login' zamiast 'username').
    """
    # Jeśli użytkownik jest już zalogowany, przekieruj go do dashboardu/projektów
    if request.user.is_authenticated:
        return redirect('web:project_list')

    if request.method == "POST":
        login_input = request.POST.get("login")
        password_input = request.POST.get("password")

        # 1. Używamy authenticate(), który pod spodem woła Twój LoginBackend
        user = authenticate(request, login=login_input, password=password_input)

        if user is not None:
            if user.is_active:
                # 2. Tworzymy sesję Django (ciasteczko sessionid)
                login(request, user)
                messages.success(request, f"Witaj ponownie, {user.name}!")

                # Obsługa parametru ?next= (przekierowanie po wymuszonym logowaniu)
                next_url = request.GET.get('next')
                if next_url:
                    return redirect(next_url)
                return redirect('web:project_list')
            else:
                messages.error(request, "Konto jest nieaktywne.")
        else:
            messages.error(request, "Błędny login lub hasło.")

    return render(request, 'web/auth/login.html')


def logout_view(request):
    """
    Wylogowuje użytkownika i czyści sesję.
    """
    logout(request)
    messages.info(request, "Wylogowano pomyślnie.")
    return redirect('web:login')