from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from domain.exceptions.exceptions import PermissionDenied
from .utils import get_container, get_domain_user


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

        # Pobieranie pól specyficznych
        severity = request.POST.get("severity") if task_type == "bug" else None
        story_points = request.POST.get("story_points") if task_type == "feature" else None

        # Konwersja story_points na int, jeśli podano
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
            messages.success(request, "Zadanie zostało dodane.")
            return redirect("web:project_detail", pk=project_id)

        except PermissionDenied as e:
            messages.error(request, f"Brak uprawnień: {str(e)}")
        except ValueError as e:
            messages.error(request, f"Błąd danych: {str(e)}")
        except Exception as e:
            messages.error(request, f"Wystąpił błąd: {str(e)}")

    return render(request, "web/tasks/create.html", {"project": project})


@login_required(login_url='web:login')
def task_move(request, pk, new_status):
    container = get_container()
    domain_user = get_domain_user(request)

    # Mapowanie statusów (tak jak miałeś)
    status_map = {"todo": "To Do", "in_progress": "In Progress", "done": "Done"}
    domain_status = status_map.get(new_status, new_status)

    try:
        task = container.tasks.task_repo.get_by_id(str(pk))
        if task:
            container.tasks.update_status(task, domain_user, domain_status)

            # --- LOGIKA HTMX ---
            if request.headers.get('HX-Request'):
                # Jeśli to HTMX, nie przeładowujemy strony.
                # Musimy odświeżyć tablicę Kanban.
                # Pobieramy projekt i dane boarda na nowo.
                project = container.project_service.get_project(task.get_project_id())

                # Używamy serwisu backlog (jak w project_detail)
                try:
                    board_data = container.backlog.kanban_board(project, domain_user)
                except AttributeError:
                    # Fallback
                    from application.backlog_service import BacklogService
                    backlog = BacklogService(container.auth, container.tasks.task_repo)
                    board_data = backlog.kanban_board(project, domain_user)

                kanban_context = {
                    "todo": board_data.get("To Do", []),
                    "in_progress": board_data.get("In Progress", []),
                    "done": board_data.get("Done", []),
                    "blocked": board_data.get("Blocked", [])
                }

                # Zwracamy TYLKO fragment HTML z tablicą (partials)
                return render(request, "web/projects/partials/kanban_board.html", {
                    "project": project,
                    "kanban": kanban_context
                })

            # Jeśli to zwykłe żądanie (nie HTMX), robimy redirect
            messages.success(request, f"Status zmieniony na {domain_status}")
            return redirect("web:project_detail", pk=task.get_project_id())

    except Exception as e:
        # W przypadku błędu HTMX, można zwrócić Toast z błędem (zaawansowane)
        # Tu prosty fallback
        messages.error(request, str(e))
        return redirect("web:project_list")