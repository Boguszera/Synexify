# infrastructure/api/views/projects.py

from rest_framework import viewsets, status
from rest_framework.response import Response
from infrastructure.api.serializers.project_serializers import ProjectSerializer
from infrastructure.di import Container

container = Container()

class ProjectViewSet(viewsets.ViewSet):

    def list(self, request):
        projects = container.admin_panel.list_projects()
        serializer = ProjectSerializer(projects, many=True)
        return Response(serializer.data)

    def retrieve(self, request, pk=None):
        project = container.project_repo.get_by_id(pk)
        if not project:
            return Response({"detail": "Not found"}, status=status.HTTP_404_NOT_FOUND)
        serializer = ProjectSerializer(project)
        return Response(serializer.data)

    def create(self, request):
        project = container.admin_panel.create_project(
            name=request.data["name"],
            description=request.data.get("description", ""),
            manager=None
        )
        serializer = ProjectSerializer(project)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def update(self, request, pk=None):
        project = container.project_repo.get_by_id(pk)
        updated_project = container.admin_panel.update_project(project, **request.data)
        serializer = ProjectSerializer(updated_project)
        return Response(serializer.data)

    def destroy(self, request, pk=None):
        container.admin_panel.delete_project(container.project_repo.get_by_id(pk))
        return Response(status=status.HTTP_204_NO_CONTENT)
