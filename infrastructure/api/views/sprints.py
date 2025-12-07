# infrastructure/api/views/sprints.py

from rest_framework import viewsets, status
from rest_framework.response import Response
from infrastructure.api.serializers.sprint_serializers import SprintSerializer
from infrastructure.di import Container

container = Container()

class SprintViewSet(viewsets.ViewSet):
    """CRUD Sprint"""

    def list(self, request):
        sprints = container.sprints.get_all()
        serializer = SprintSerializer(sprints, many=True)
        return Response(serializer.data)

    def retrieve(self, request, pk=None):
        sprint = container.sprints.get_by_id(pk)
        if not sprint:
            return Response({"detail": "Not found"}, status=status.HTTP_404_NOT_FOUND)
        serializer = SprintSerializer(sprint)
        return Response(serializer.data)

    def create(self, request):
        project = container.project_repo.get_by_id(request.data["project_id"])
        sprint = container.sprints.create_sprint(
            project=project,
            name=request.data["name"],
            start_date=request.data["start_date"],
            end_date=request.data["end_date"]
        )
        serializer = SprintSerializer(sprint)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def update(self, request, pk=None):
        sprint = container.sprints.get_by_id(pk)
        sprint.name = request.data.get("name", sprint.get_name())
        sprint.start_date = request.data.get("start_date", getattr(sprint, "_start_date", None))
        sprint.end_date = request.data.get("end_date", getattr(sprint, "_end_date", None))
        container.sprints.save(sprint)
        serializer = SprintSerializer(sprint)
        return Response(serializer.data)

    def destroy(self, request, pk=None):
        container.sprints.delete(pk)
        return Response(status=status.HTTP_204_NO_CONTENT)
