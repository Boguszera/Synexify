from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import HttpResponseForbidden

from domain.exceptions.exceptions import PermissionDenied
from .utils import get_container, get_domain_user
from application.backlog_service import BacklogService


@login_required(login_url='web:login')
def sprint_create(request, project_id):
    container = get_container()
    domain_user = get_domain_user(request)

    project = container.project_service.get_project(str(project_id))
    if not project:
        messages.error(request, "The project does not exist.")
        return redirect("web:project_list")

    if not container.auth.can_manage_project(domain_user, project):
        return HttpResponseForbidden("You do not have permission to manage sprints on this project.")

    if request.method == "POST":
        name = request.POST.get("name")
        start_date = request.POST.get("start_date")
        end_date = request.POST.get("end_date")

        try:
            container.sprints.create_sprint(
                project=project,
                name=name,
                start_date=start_date,
                end_date=end_date,
                user=domain_user
            )
            messages.success(request, f"Sprint '{name}' was successfully created.")
            return redirect("web:project_detail", pk=project_id)

        except PermissionDenied as e:
            messages.error(request, f"No permissions: {str(e)}")
        except Exception as e:
            messages.error(request, f"Sprint creation error: {str(e)}")

    return render(request, "web/sprints/create.html", {"project": project})


@login_required(login_url='web:login')
def sprint_board(request, pk):
    container = get_container()
    domain_user = get_domain_user(request)

    sprint = container.sprints.get_sprint(str(pk))
    if not sprint:
        messages.error(request, "Sprint doesn't exist.")
        return redirect('web:project_list')

    project = container.project_service.get_project(sprint.get_project_id())
    if not container.project_service.can_view(domain_user, project):
        return HttpResponseForbidden("You do not have access to this sprint.")

    backlog_service = getattr(container, 'backlog',
                              BacklogService(container.auth,
                                             container.tasks.task_repo,
                                             container.sprints.sprint_repo))
    board_data = backlog_service.kanban_board(project, domain_user, sprint_id=sprint.get_id())

    kanban_context = {
        "todo": board_data.get("To Do", []),
        "in_progress": board_data.get("In Progress", []),
        "done": board_data.get("Done", []),
        "blocked": board_data.get("Blocked", [])
    }

    return render(request, "web/sprints/board.html", {
        "project": project,
        "sprint": sprint,
        "kanban": kanban_context
    })