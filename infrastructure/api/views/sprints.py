# infrastructure/api/views/sprints.py
from rest_framework import viewsets, status
from rest_framework.response import Response
from infrastructure.api.serializers.sprint_serializers import SprintSerializer
from infrastructure.adapters.user_adapter import to_domain_user
from domain.exceptions.exceptions import PermissionDenied

class SprintViewSet(viewsets.ViewSet):
    """CRUD Sprint"""

    def get_container(self):
        from infrastructure.di import Container
        return Container()

    def list(self, request):
        container = self.get_container()
        try:
            domain_user = to_domain_user(request.user)
            sprints = container.sprints.get_all(user=domain_user)  # filtracja po uprawnieniach
            serializer = SprintSerializer(sprints, many=True)
            return Response(serializer.data)
        except PermissionDenied as e:
            return Response({"detail": str(e)}, status=status.HTTP_403_FORBIDDEN)

    def retrieve(self, request, pk=None):
        container = self.get_container()
        try:
            domain_user = to_domain_user(request.user)
            sprint = container.sprints.get_by_id(pk)
            if not sprint:
                return Response({"detail": "Not found"}, status=status.HTTP_404_NOT_FOUND)

            # sprawdzamy dostęp
            container.sprints.check_view_permission(domain_user, sprint)
            serializer = SprintSerializer(sprint)
            return Response(serializer.data)
        except PermissionDenied as e:
            return Response({"detail": str(e)}, status=status.HTTP_403_FORBIDDEN)

    def create(self, request):
        container = self.get_container()
        try:
            domain_user = to_domain_user(request.user)
            project = container.project_repo.get_by_id(request.data["project_id"])
            sprint = container.sprints.create_sprint(
                project=project,
                name=request.data["name"],
                start_date=request.data["start_date"],
                end_date=request.data["end_date"],
                user=domain_user
            )
            serializer = SprintSerializer(sprint)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        except PermissionDenied as e:
            return Response({"detail": str(e)}, status=status.HTTP_403_FORBIDDEN)

    def update(self, request, pk=None):
        container = self.get_container()
        try:
            domain_user = to_domain_user(request.user)
            sprint = container.sprints.get_by_id(pk)
            updated_sprint = container.sprints.update_sprint(
                sprint,
                name=request.data.get("name", sprint.get_name()),
                start_date=request.data.get("start_date", getattr(sprint, "_start_date", None)),
                end_date=request.data.get("end_date", getattr(sprint, "_end_date", None)),
                user=domain_user
            )
            serializer = SprintSerializer(updated_sprint)
            return Response(serializer.data)
        except PermissionDenied as e:
            return Response({"detail": str(e)}, status=status.HTTP_403_FORBIDDEN)

    def destroy(self, request, pk=None):
        container = self.get_container()
        try:
            domain_user = to_domain_user(request.user)
            sprint = container.sprints.get_by_id(pk)
            container.sprints.delete_sprint(sprint, user=domain_user)
            return Response(status=status.HTTP_204_NO_CONTENT)
        except PermissionDenied as e:
            return Response({"detail": str(e)}, status=status.HTTP_403_FORBIDDEN)
