# infrastructure/web/views/project_views.py

from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from infrastructure.di import Container
from infrastructure.adapters.user_adapter import to_domain_user
from domain.exceptions.exceptions import PermissionDenied


# Helper do kontenera
def get_container():
    return Container()


@login_required
def project_list(request):
    container = get_container()
    domain_user = to_domain_user(request.user)

    # 1. Pobieramy dane z serwisu (tak samo jak w API!)
    try:
        # Uwaga: project_service zwraca obiekty domenowe
        projects = container.project_service.list_projects(user=domain_user)

        # 2. Renderujemy HTML
        return render(request, 'web/projects/list.html', {
            'projects': projects
        })
    except Exception as e:
        messages.error(request, f"Błąd pobierania projektów: {e}")
        return render(request, 'web/projects/list.html', {'projects': []})


@login_required
def project_create(request):
    if request.method == "POST":
        container = get_container()
        domain_user = to_domain_user(request.user)
        name = request.POST.get("name")
        description = request.POST.get("description")

        try:
            container.project_service.create_project(
                name=name,
                description=description,
                user=domain_user
            )
            messages.success(request, "Projekt utworzony pomyślnie.")
            return redirect('web:project_list')
        except PermissionDenied:
            messages.error(request, "Brak uprawnień do tworzenia projektu.")
        except Exception as e:
            messages.error(request, f"Wystąpił błąd: {e}")

    return render(request, 'web/projects/create.html')


@login_required
def project_detail(request, pk):
    container = get_container()
    domain_user = to_domain_user(request.user)

    project = container.project_service.get_project(pk)
    if not project:
        return render(request, '404.html', status=404)

    # Sprawdzenie uprawnień (można użyć helpera z serwisu lub permission class logic)
    if not container.project_service.can_view(domain_user, project):
        return render(request, '403.html', status=403)

    # Pobierz sprinty i taski dla widoku szczegółowego
    sprints = container.sprint_repo.list_by_project(pk)
    tasks = container.task_repo.list_by_project(pk)

    return render(request, 'web/projects/detail.html', {
        'project': project,
        'sprints': sprints,
        'tasks': tasks
    })