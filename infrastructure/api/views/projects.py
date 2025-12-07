# infrastructure/api/views/projects.py
from rest_framework import viewsets, status
from rest_framework.response import Response
from infrastructure.api.serializers.project_serializers import ProjectSerializer
from infrastructure.adapters.user_adapter import to_domain_user
from domain.exceptions.exceptions import PermissionDenied

class ProjectViewSet(viewsets.ViewSet):
    def get_container(self):
        from infrastructure.di import Container
        return Container()

    def list(self, request):
        container = self.get_container()
        try:
            domain_user = to_domain_user(request.user)
            projects = container.admin_panel.list_projects(user=domain_user)
            serializer = ProjectSerializer(projects, many=True)
            return Response(serializer.data)
        except PermissionDenied as e:
            return Response({"detail": str(e)}, status=status.HTTP_403_FORBIDDEN)

    def retrieve(self, request, pk=None):
        container = self.get_container()
        try:
            domain_user = to_domain_user(request.user)
            project = container.project_repo.get_by_id(pk)
            if not project:
                return Response({"detail": "Not found"}, status=status.HTTP_404_NOT_FOUND)
            container.auth.check_view_project(domain_user, project)
            serializer = ProjectSerializer(project)
            return Response(serializer.data)
        except PermissionDenied as e:
            return Response({"detail": str(e)}, status=status.HTTP_403_FORBIDDEN)

    def create(self, request):
        container = self.get_container()
        try:
            domain_user = to_domain_user(request.user)
            project = container.admin_panel.create_project(
                name=request.data["name"],
                description=request.data.get("description", ""),
                user=domain_user
            )
            serializer = ProjectSerializer(project)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        except PermissionDenied as e:
            return Response({"detail": str(e)}, status=status.HTTP_403_FORBIDDEN)

    def update(self, request, pk=None):
        container = self.get_container()
        try:
            domain_user = to_domain_user(request.user)
            project = container.project_repo.get_by_id(pk)
            updated_project = container.admin_panel.update_project(project, request.data, user=domain_user)
            serializer = ProjectSerializer(updated_project)
            return Response(serializer.data)
        except PermissionDenied as e:
            return Response({"detail": str(e)}, status=status.HTTP_403_FORBIDDEN)

    def destroy(self, request, pk=None):
        container = self.get_container()
        try:
            domain_user = to_domain_user(request.user)
            project = container.project_repo.get_by_id(pk)
            container.admin_panel.delete_project(project, user=domain_user)
            return Response(status=status.HTTP_204_NO_CONTENT)
        except PermissionDenied as e:
            return Response({"detail": str(e)}, status=status.HTTP_403_FORBIDDEN)
