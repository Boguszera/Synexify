# infrastructure/web/views/report_views.py

from django.contrib.auth.decorators import login_required
from django.shortcuts import render

from .utils import get_container, get_domain_user


@login_required(login_url="web:login")
def report_status_summary(request):
    container = get_container()
    domain_user = get_domain_user(request)
    status_data = container.reporting.get_task_status_summary_all(domain_user)

    return render(
        request, "web/reports/status_summary.html", {"status_data": status_data, "title": "Task Status Summary"}
    )


@login_required(login_url="web:login")
def report_team_workload(request):
    container = get_container()
    domain_user = get_domain_user(request)

    project_id = request.GET.get("project_id")

    workload_data = container.reporting.get_team_workload_summary(domain_user, project_id=project_id)

    all_projects = container.project_repo.list_all()
    visible_projects = [p for p in all_projects if container.auth.can_view_project(domain_user, p)]

    return render(
        request,
        "web/reports/team_workload.html",
        {
            "workload_data": workload_data,
            "all_projects": visible_projects,
            "selected_project_id": project_id,
            "title": "Team Load",
        },
    )


@login_required(login_url="web:login")
def report_team_velocity(request):
    return render(request, "web/reports/team_velocity.html", {"title": "Team Speed (In Progress)"})
