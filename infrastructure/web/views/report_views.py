# infrastructure/web/views/report_views.py

from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .utils import get_container, get_domain_user


@login_required(login_url='web:login')
def report_status_summary(request):
    container = get_container()
    domain_user = get_domain_user(request)

    # Używamy nowej metody
    status_data = container.reporting.get_task_status_summary_all(domain_user)

    return render(request, "web/reports/status_summary.html", {
        'status_data': status_data,
        'title': 'Podsumowanie Statusów Zadań'
    })


@login_required(login_url='web:login')
def report_team_workload(request):
    container = get_container()
    domain_user = get_domain_user(request)

    # Pobieramy ID projektu z query string (opcjonalnie)
    project_id = request.GET.get('project_id')

    # Używamy nowej metody
    workload_data = container.reporting.get_team_workload_summary(domain_user, project_id=project_id)

    # Opcjonalnie: pobieranie listy projektów dla filtra
    all_projects = container.project_repo.list_all()

    return render(request, "web/reports/team_workload.html", {
        'workload_data': workload_data,
        'all_projects': all_projects,
        'selected_project_id': project_id,
        'title': 'Obciążenie Zespołu'
    })


# Na razie Team Velocity zostawiamy jako placeholder, gdyż logika jest skomplikowana
@login_required(login_url='web:login')
def report_team_velocity(request):
    return render(request, "web/reports/team_velocity.html", {'title': 'Prędkość Zespołu (W budowie)'})