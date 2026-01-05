from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from .utils import get_container, get_domain_user


def login_view(request):
    if request.method == "POST":
        login_str = request.POST.get("login")
        password = request.POST.get("password")

        # standard Django mechanism for session auth
        user = authenticate(request, login=login_str, password=password)

        if user is not None:
            login(request, user)
            return redirect("web:project_list")
        else:
            messages.error(request, "Incorrect login or password.")

    return render(request, "web/auth/login.html")


def logout_view(request):
    logout(request)
    return redirect("web:login")