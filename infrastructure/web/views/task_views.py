from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.template.loader import render_to_string
from django.http import HttpResponse  # HTMX
from domain.exceptions.exceptions import PermissionDenied
from .utils import get_container, get_domain_user
from application.backlog_service import BacklogService


@login_required(login_url='web:login')
def task_create(request, project_id):
    container = get_container()
    domain_user = get_domain_user(request)

    project = container.project_service.get_project(str(project_id))
    if not project:
        return redirect("web:project_list")

    if request.method == "POST":
        title = request.POST.get("title")
        description = request.POST.get("description", "")
        task_type = request.POST.get("task_type", "chore")
        severity = request.POST.get("severity") if task_type == "bug" else None
        story_points = request.POST.get("story_points") if task_type == "feature" else None

        if story_points:
            try:
                story_points = int(story_points)
            except ValueError:
                story_points = None

        try:
            container.tasks.create_task(
                project=project,
                title=title,
                description=description,
                task_type=task_type,
                user=domain_user,
                severity=severity,
                story_points=story_points
            )
            messages.success(request, "Task has been added.")
            return redirect("web:project_detail", pk=project_id)

        except PermissionDenied as e:
            messages.error(request, f"No permissions: {str(e)}")
        except ValueError as e:
            messages.error(request, f"Data error:{str(e)}")
        except Exception as e:
            messages.error(request, f"An error occurred: {str(e)}")

    return render(request, "web/tasks/create.html", {"project": project})


@login_required(login_url='web:login')
def task_move(request, pk, new_status):
    container = get_container()
    domain_user = get_domain_user(request)
    status_slug = new_status

    if status_slug not in ["todo", "in_progress", "done", "blocked"]:
        messages.error(request, f"Unknown slug status: {status_slug}")
        return redirect("web:project_list")

    try:
        task = container.tasks.task_repo.get_by_id(str(pk))
        if not task:
            messages.error(request, "The task does not exist.")
            return redirect("web:project_list")
        updated_task = container.tasks.update_status(task, domain_user, status_slug)

        sprint_id = updated_task.get_sprint_id()
        project = container.project_service.get_project(updated_task.get_project_id())

        if request.headers.get('HX-Request'):
            backlog_service = getattr(container, 'backlog',
                                      BacklogService(container.auth,
                                                     container.tasks.task_repo,
                                                     container.sprints.sprint_repo))
            board_data = backlog_service.kanban_board(project, domain_user, sprint_id=sprint_id)

            kanban_context = {
                "todo": board_data.get("To Do", []),
                "in_progress": board_data.get("In Progress", []),
                "done": board_data.get("Done", []),
                "blocked": board_data.get("Blocked", [])
            }

            return render(request, "web/projects/partials/kanban_board.html", {
                "project": project,
                "kanban": kanban_context
            })
        messages.success(request, f"Status changed to {updated_task.get_status()}")

        if sprint_id:
            return redirect('web:sprint_board', pk=sprint_id)
        else:
            return redirect('web:project_detail', pk=project.get_id())

    except PermissionDenied as e:
        messages.error(request, str(e))
        if 'task' in locals() and task:
            if task.get_sprint_id():
                return redirect('web:sprint_board', pk=task.get_sprint_id())
            else:
                return redirect('web:project_detail', pk=task.get_project_id())

        return redirect("web:project_list")

    except Exception as e:
        messages.error(request, f"An error occurred while changing status:{type(e).__name__} - {str(e)}")

        if 'task' in locals() and task:
            if task.get_sprint_id():
                return redirect('web:sprint_board', pk=task.get_sprint_id())
            else:
                return redirect('web:project_detail', pk=task.get_project_id())

        return redirect("web:project_list")

@login_required(login_url='web:login')
def task_detail(request, pk):
    container = get_container()
    domain_user = get_domain_user(request)

    task = container.tasks.task_repo.get_by_id(str(pk))
    if not task:
        messages.error(request, "Task does not exist.")
        return redirect('web:project_list')
    project = container.project_service.get_project(task.get_project_id())
    if not project or not container.project_service.can_view(domain_user, project):
        messages.error(request, "No access to the project.")
        return redirect('web:login')
    comments = container.comments.list_comments_for_task(task.get_id(), domain_user)
    attachments = container.attachments.list_attachments_for_task(task.get_id(), domain_user)

    try:
        all_users = container.user_repo.list_all()
    except Exception as e:
        messages.warning(request, f"Error loading user list:{str(e)}")
        all_users = []

    current_assignee_ids = task.get_assignees_ids()
    assignees = []
    if current_assignee_ids:
        for uid in current_assignee_ids:
            u = container.user_repo.get_by_id(uid)
            if u: assignees.append(u)

    return render(request, "web/tasks/detail.html", {
        "task": task,
        "project": project,
        "comments": comments,
        "attachments": attachments,
        "all_users": all_users,
        "assignees": assignees
    })


@login_required(login_url='web:login')
def add_comment(request, pk):
    if request.method == "POST":
        container = get_container()
        domain_user = get_domain_user(request)
        content = request.POST.get("content")

        try:
            task = container.tasks.task_repo.get_by_id(str(pk))
            container.tasks.add_comment(task, domain_user, content)
            messages.success(request, "Comment added.")
        except Exception as e:
            messages.error(request, f"Error: {str(e)}")

    return redirect('web:task_detail', pk=pk)


@login_required(login_url='web:login')
def add_attachment(request, pk):
    if request.method == "POST" and request.FILES.get("file"):
        container = get_container()
        domain_user = get_domain_user(request)
        file = request.FILES["file"]

        try:
            container.attachments.add_attachment(str(pk), domain_user, file)
            messages.success(request, "File added.")
        except Exception as e:
            messages.error(request, f"Error: {str(e)}")

    return redirect('web:task_detail', pk=pk)


@login_required(login_url='web:login')
def assign_task(request, pk):
    if request.method == "POST":
        container = get_container()
        domain_user = get_domain_user(request)
        assignee_id = request.POST.get("assignee_id")

        try:
            task = container.tasks.task_repo.get_by_id(str(pk))
            if not task:
                messages.error(request, "The task does not exist.")
                return redirect('web:project_list')

            if not assignee_id:
                raise ValueError("User ID required for assignment.")

            container.tasks.assign_task_by_id(task, domain_user, assignee_id)
            messages.success(request, f"The task has been assigned.")

        except PermissionDenied as e:
            messages.error(request, f"No permission to assign task:{str(e)}")
        except ValueError as e:
            messages.error(request, f"Assignment error: {str(e)}")
        except Exception as e:
            messages.error(request, f"An unknown error occurred: {str(e)}")

    return redirect('web:task_detail', pk=pk)


@login_required(login_url='web:login')
def add_task_to_sprint(request, pk):
    if request.method == "POST":
        container = get_container()
        domain_user = get_domain_user(request)
        sprint_id = request.POST.get("sprint_id")

        try:
            task = container.tasks.task_repo.get_by_id(str(pk))
            sprint = container.sprints.get_sprint(sprint_id)

            if not task or not sprint:
                messages.error(request, "The task or sprint does not exist.")
                return redirect('web:project_list')
            container.sprints.add_task_to_sprint(sprint, task, user=domain_user)
            messages.success(request, f"The task'{task.get_title()}' was added to the sprint '{sprint.get_name()}'.")
            return redirect('web:project_detail', pk=task.get_project_id())

        except PermissionDenied as e:
            messages.error(request, f"No permissions to manage sprints:{str(e)}")
        except Exception as e:
            messages.error(request, f"Error adding to sprint: {str(e)}")
    return redirect('web:task_detail', pk=pk)


@login_required(login_url='web:login')
def unassign_task(request, pk, assignee_id):
    if request.method == "POST":
        container = get_container()
        domain_user = get_domain_user(request)

        try:
            task = container.tasks.task_repo.get_by_id(str(pk))
            if not task:
                messages.error(request, "The task does not exist.")
                return redirect('web:project_list')
            container.tasks.unassign_user_by_id(task, domain_user, assignee_id)
            messages.success(request, f"Assignment removed.")

        except PermissionDenied as e:
            messages.error(request, f"No permission to remove assignment: {str(e)}")
        except ValueError as e:
            messages.error(request, f"Unassignment error:{str(e)}")
        except Exception as e:
            messages.error(request, f"An unknown error occurred:{str(e)}")

    return redirect('web:task_detail', pk=pk)


@login_required(login_url='web:login')
def my_assignments(request):
    container = get_container()
    domain_user = get_domain_user(request)
    all_tasks = container.tasks.task_repo.get_all()
    user_id = domain_user.get_id()

    assigned_tasks = [
        t for t in all_tasks
        if user_id in t.get_assignees_ids()
    ]

    context = {
        'tasks': assigned_tasks,
        'title': 'My Assigned Tasks',
        'current_user': domain_user
    }

    return render(request, "web/tasks/my_assignments.html", context)

@login_required(login_url='web:login')
def remove_task_from_sprint(request, pk):
    if request.method == "POST":
        container = get_container()
        domain_user = get_domain_user(request)

        try:
            task = container.tasks.task_repo.get_by_id(str(pk))
            if not task:
                messages.error(request, "Task does not exist.")
                return redirect('web:project_list')

            sprint_id = task.get_sprint_id()
            if not sprint_id:
                messages.warning(request, "This task is not assigned.")
                return redirect('web:task_detail', pk=pk)

            sprint = container.sprints. get_sprint(sprint_id)
            if not sprint:
                messages.error(request, "Sprint does not exist.")
                return redirect('web:task_detail', pk=pk)

            container.sprints.remove_task_from_sprint(sprint, task, user=domain_user)
            messages.success(request, "Task removed from sprint.")
            return redirect('web:task_detail', pk=pk)

        except PermissionDenied as e:
            messages.error(request, f"No permissions:  {str(e)}")
            return redirect('web:task_detail', pk=pk)
        except Exception as e:
            messages.error(request, f"Error:  {str(e)}")
            return redirect('web:task_detail', pk=pk)

    return redirect('web:task_detail', pk=pk)