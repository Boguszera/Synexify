# infrastructure/api/views/sprints.py

from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import action
from infrastructure.api.serializers.sprint_serializers import SprintSerializer
from infrastructure.adapters.user_adapter import to_domain_user
from infrastructure.api.permissions.sprint_permissions import SprintPermissions
from infrastructure.api.permissions.project_permissions import ProjectPermissions
from infrastructure.api.serializers.task_serializers import TaskSerializer
from domain.exceptions.exceptions import PermissionDenied

class SprintViewSet(viewsets.ViewSet):
    """CRUD Sprint"""

    def get_container(self):
        from infrastructure.di import Container
        return Container()

    def list(self, request):
        container = self.get_container()
        domain_user = to_domain_user(request.user)
        all_sprints = container.sprints.list_sprints(user=domain_user)
        serializer = SprintSerializer(all_sprints, many=True)
        return Response(serializer.data)

    def retrieve(self, request, pk=None):
        container = self.get_container()
        domain_user = to_domain_user(request.user)
        sprint = container.sprints.get_sprint(pk)
        if not sprint:
            return Response({"detail": "Not found"}, status=404)
        serializer = SprintSerializer(sprint)
        return Response(serializer.data)

    def create(self, request):
        container = self.get_container()
        domain_user = to_domain_user(request.user)
        project = container.project_service.get_project(request.data["project_id"])
        if not project or not SprintPermissions.can_create(domain_user, project):
            return Response({"detail": "Forbidden"}, status=403)
        sprint = container.sprints.create_sprint(
            project=project,
            name=request.data["name"],
            start_date=request.data["start_date"],
            end_date=request.data["end_date"],
            user=domain_user
        )
        serializer = SprintSerializer(sprint)
        return Response(serializer.data, status=201)

    def update(self, request, pk=None):
        container = self.get_container()
        domain_user = to_domain_user(request.user)
        sprint = container.sprints.get_sprint(pk)
        if not sprint:
            return Response({"detail": "Not found"}, status=404)
        updated_sprint = container.sprints.update_sprint(
            sprint,
            {
                "name": request.data.get("name", sprint.get_name()),
                "start_date": request.data.get("start_date", getattr(sprint, "_start_date", None)),
                "end_date": request.data.get("end_date", getattr(sprint, "_end_date", None))
            },
            user=domain_user
        )
        serializer = SprintSerializer(updated_sprint)
        return Response(serializer.data)

    def destroy(self, request, pk=None):
        container = self.get_container()
        domain_user = to_domain_user(request.user)
        sprint = container.sprints.get_sprint(pk)
        if not sprint:
            return Response({"detail": "Not found"}, status=404)
        container.sprints.delete_sprint(sprint, user=domain_user)
        return Response(status=204)

    @action(detail=True, methods=["post"])
    def add_task(self, request, pk=None):
        """
        POST /api/sprints/{id}/add_task/
        Body: {"task_id": "uuid"}
        """
        container = self.get_container()
        domain_user = to_domain_user(request.user)

        sprint = container.sprints.get_sprint(pk)
        if not sprint:
            return Response({"detail": "Sprint not found"}, status=404)

        task_id = request.data.get("task_id")
        if not task_id:
            return Response({"detail": "task_id is required"}, status=400)

        task = container.tasks.task_repo.get_by_id(task_id)
        if not task:
            return Response({"detail": "Task not found"}, status=404)

        try:
            container.sprints.add_task_to_sprint(sprint, task, user=domain_user)
            return Response({"status": "Task added to sprint"}, status=200)
        except PermissionDenied as e:
            return Response({"detail": str(e)}, status=403)
        except Exception as e:
            return Response({"detail": str(e)}, status=400)

    @action(detail=True, methods=["get"])
    def tasks(self, request, pk=None):
        """
        GET /api/sprints/{id}/tasks/
        Dodano weryfikację uprawnień opartą na dostępie do projektu.
        """
        container = self.get_container()
        domain_user = to_domain_user(request.user)

        sprint = container.sprints.get_sprint(pk)
        if not sprint:
            return Response({"detail": "Sprint not found"}, status=status.HTTP_404_NOT_FOUND)

        project = container.project_service.get_project(sprint.get_project_id())
        if not project:
            return Response({"detail": "Project not found for this sprint"}, status=status.HTTP_404_NOT_FOUND)

        if not ProjectPermissions.can_view(domain_user, project):
            return Response({"detail": "Forbidden: User cannot view tasks in this project's sprint"},
                            status=status.HTTP_403_FORBIDDEN)

        tasks = container.tasks.task_repo.list_by_sprint(pk)
        serializer = TaskSerializer(tasks, many=True)
        return Response(serializer.data)
