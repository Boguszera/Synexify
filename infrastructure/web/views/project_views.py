from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import HttpResponseForbidden

from domain.exceptions.exceptions import PermissionDenied
from .utils import get_container, get_domain_user
from application.backlog_service import BacklogService


@login_required(login_url='web:login')
def project_list(request):
    container = get_container()
    domain_user = get_domain_user(request)

    try:
        projects = container.project_service.list_projects(user=domain_user)
    except PermissionDenied as e:
        messages.error(request, f"No permissions: {str(e)}")
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
            messages.success(request, "The project has been created.")
            return redirect("web:project_list")
        except PermissionDenied:
            messages.error(request, "You do not have permission to create projects.")
        except Exception as e:
            messages.error(request, f"Error: {str(e)}")

    return render(request, "web/projects/create.html")


@login_required(login_url='web:login')
def project_detail(request, pk):
    container = get_container()
    domain_user = get_domain_user(request)
    project = container.project_service.get_project(str(pk))

    if not project or not container. auth.can_view_project(domain_user, project):
        return HttpResponseForbidden("Access denied or project does not exist.")

    backlog_service = getattr(container, 'backlog',
                              BacklogService(container.auth,
                                             container.tasks.task_repo,
                                             container.sprints.sprint_repo))
    sprints = []
    for s_id in project.get_sprint_ids():
        s = container.sprints.get_sprint(s_id)
        if s: sprints.append(s)
    try:
        backlog_tasks = backlog_service.get_backlog(project, domain_user)
    except Exception as e:
        messages.warning(request, f"Backlog loading error: {str(e)}")
        backlog_tasks = []


    return render(request, "web/projects/dashboard.html", {
        "project": project,
        "sprints": sprints,
        "backlog": backlog_tasks
    })