from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import HttpResponseForbidden

from domain.exceptions.exceptions import PermissionDenied
from .utils import get_container, get_domain_user


@login_required(login_url='web:login')
def sprint_create(request, project_id):
    container = get_container()
    domain_user = get_domain_user(request)

    project = container.project_service.get_project(str(project_id))
    if not project:
        messages.error(request, "Projekt nie istnieje.")
        return redirect("web:project_list")

    # Podstawowa weryfikacja uprawnień przed próbą utworzenia
    if not container.auth.can_manage_project(domain_user, project):
        return HttpResponseForbidden("Brak uprawnień do zarządzania sprintami w tym projekcie.")

    if request.method == "POST":
        name = request.POST.get("name")
        start_date = request.POST.get("start_date")
        end_date = request.POST.get("end_date")

        try:
            # Użycie SprintService do utworzenia nowego sprintu
            container.sprints.create_sprint(
                project=project,
                name=name,
                start_date=start_date,
                end_date=end_date,
                user=domain_user
            )
            messages.success(request, f"Sprint '{name}' został pomyślnie utworzony.")
            return redirect("web:project_detail", pk=project_id)

        except PermissionDenied as e:
            messages.error(request, f"Brak uprawnień: {str(e)}")
        except Exception as e:
            messages.error(request, f"Błąd tworzenia sprintu: {str(e)}")

    return render(request, "web/sprints/create.html", {"project": project})