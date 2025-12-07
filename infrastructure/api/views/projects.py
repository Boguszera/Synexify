from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from infrastructure.di import Container
from infrastructure.api.serializers.project_serializers import ProjectSerializer, ProjectCreateUpdateSerializer

container = Container()

class ProjectListCreateAPIView(APIView):
    def get(self, request):
        projects = container.project_repo.list_all()
        serializer = ProjectSerializer(projects, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = ProjectCreateUpdateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = serializer.validated_data
        project = container.admin_panel.create_project(
            name=data['name'],
            description=data['description']
        )
        output_serializer = ProjectSerializer(project)
        return Response(output_serializer.data, status=status.HTTP_201_CREATED)


class ProjectDetailAPIView(APIView):
    def get(self, request, project_id):
        project = container.project_repo.get_by_id(project_id)
        if not project:
            return Response({"detail": "Project not found"}, status=status.HTTP_404_NOT_FOUND)
        serializer = ProjectSerializer(project)
        return Response(serializer.data)

    def put(self, request, project_id):
        project = container.project_repo.get_by_id(project_id)
        if not project:
            return Response({"detail": "Project not found"}, status=status.HTTP_404_NOT_FOUND)
        serializer = ProjectCreateUpdateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = serializer.validated_data
        updated_project = container.admin_panel.update_project(project, **data)
        output_serializer = ProjectSerializer(updated_project)
        return Response(output_serializer.data)

    def delete(self, request, project_id):
        project = container.project_repo.get_by_id(project_id)
        if not project:
            return Response({"detail": "Project not found"}, status=status.HTTP_404_NOT_FOUND)
        container.admin_panel.delete_project(project)
        return Response(status=status.HTTP_204_NO_CONTENT)
