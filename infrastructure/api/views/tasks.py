from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from infrastructure.di import Container
from infrastructure.api.serializers.task_serializers import TaskSerializer, TaskCreateUpdateSerializer

container = Container()

class TaskListCreateAPIView(APIView):
    def get(self, request, project_id=None):
        tasks = container.task_repo.list_by_project(project_id)
        serializer = TaskSerializer(tasks, many=True)
        return Response(serializer.data)

    def post(self, request, project_id=None):
        serializer = TaskCreateUpdateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = serializer.validated_data
        task = container.tasks.create_task(
            project=container.project_repo.get_by_id(project_id),
            title=data['title'],
            description=data['description'],
            task_type=data['type'],
            user=request.user
        )
        output_serializer = TaskSerializer(task)
        return Response(output_serializer.data, status=status.HTTP_201_CREATED)


class TaskDetailAPIView(APIView):
    def get(self, request, task_id):
        task = container.task_repo.get_by_id(task_id)
        if not task:
            return Response({"detail": "Task not found"}, status=status.HTTP_404_NOT_FOUND)
        serializer = TaskSerializer(task)
        return Response(serializer.data)

    def put(self, request, task_id):
        task = container.task_repo.get_by_id(task_id)
        if not task:
            return Response({"detail": "Task not found"}, status=status.HTTP_404_NOT_FOUND)

        serializer = TaskCreateUpdateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = serializer.validated_data

        updated_task = container.tasks.update_task(
            task,
            title=data.get('title'),
            description=data.get('description')
        )
        output_serializer = TaskSerializer(updated_task)
        return Response(output_serializer.data)

    def delete(self, request, task_id):
        task = container.task_repo.get_by_id(task_id)
        if not task:
            return Response({"detail": "Task not found"}, status=status.HTTP_404_NOT_FOUND)
        container.task_repo.delete(task_id)
        return Response(status=status.HTTP_204_NO_CONTENT)
