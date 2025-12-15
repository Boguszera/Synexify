from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import HttpResponseForbidden

from domain.exceptions.exceptions import PermissionDenied
from .utils import get_container, get_domain_user


@login_required(login_url='web:login')
def project_list(request):
    container = get_container()
    domain_user = get_domain_user(request)

    try:
        # Pobieramy projekty z serwisu aplikacyjnego
        projects = container.project_service.list_projects(user=domain_user)
    except PermissionDenied as e:
        messages.error(request, f"Brak uprawnień: {str(e)}")
        projects = []

    return render(request, "web/projects/list.html", {"projects": projects})


@login_required(login_url='web:login')
def project_create(request):
    if request.method == "POST":
        container = get_container()
        domain_user = get_domain_user(request)

        name = request.POST.get("name")
        description = request.POST.get("description", "")

        try:
            container.project_service.create_project(
                name=name,
                description=description,
                user=domain_user
            )
            messages.success(request, "Projekt został utworzony.")
            return redirect("web:project_list")
        except PermissionDenied:
            messages.error(request, "Nie masz uprawnień do tworzenia projektów.")
        except Exception as e:
            messages.error(request, f"Błąd: {str(e)}")

    return render(request, "web/projects/create.html")


@login_required(login_url='web:login')
def project_detail(request, pk):
    """
    Ten widok obsługuje tablicę Kanban i listę sprintów.
    """
    container = get_container()
    domain_user = get_domain_user(request)

    # 1. Pobierz projekt
    project = container.project_service.get_project(str(pk))

    if not project:
        messages.error(request, "Projekt nie istnieje.")
        return redirect("web:project_list")

    # 2. Sprawdź uprawnienia do wyświetlania
    if not container.project_service.can_view(domain_user, project):
        return HttpResponseForbidden("Nie masz dostępu do tego projektu.")

    # 3. Pobierz dane do Kanbana
    try:
        # Użycie container.backlog
        board_data = container.backlog.kanban_board(project, domain_user)
    except AttributeError:
        # Fallback (powinien zostać usunięty po poprawnej konfiguracji DI)
        from application.backlog_service import BacklogService
        backlog_service = BacklogService(container.auth, container.tasks.task_repo)
        board_data = backlog_service.kanban_board(project, domain_user)
    except PermissionDenied:
        # Zabezpieczenie na wypadek, gdyby serwis z jakiegoś powodu znowu sprawdzał uprawnienia
        return HttpResponseForbidden("Nie masz dostępu do Kanbana w tym projekcie.")

    # 4. POBIERANIE DANYCH SPRINTÓW [NOWA LOGIKA]
    sprints = []
    # Zakładamy, że projekt ma listę ID sprintów, a SprintService ma metodę get_sprint
    sprint_ids = project.get_sprint_ids()
    if sprint_ids:
        for sprint_id in sprint_ids:
            sprint = container.sprints.get_sprint(sprint_id)
            if sprint:
                sprints.append(sprint)

    # 5. Mapowanie kluczy domenowych na klucze template'u
    kanban_context = {
        "todo": board_data.get("To Do", []),
        "in_progress": board_data.get("In Progress", []),
        "done": board_data.get("Done", []),
        "blocked": board_data.get("Blocked", [])
    }

    return render(request, "web/projects/detail.html", {
        "project": project,
        "kanban": kanban_context,
        "sprints": sprints,  # Przekazujemy pełne obiekty sprintów
    })