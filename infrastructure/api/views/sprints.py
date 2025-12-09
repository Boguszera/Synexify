# infrastructure/api/views/sprints.py

from rest_framework import viewsets, status
from rest_framework.response import Response
from infrastructure.api.serializers.sprint_serializers import SprintSerializer
from infrastructure.adapters.user_adapter import to_domain_user
from infrastructure.api.permissions.sprint_permissions import SprintPermissions

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
