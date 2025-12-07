# infrastructure/api/views/tasks.py

from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import action

from infrastructure.api.serializers.task_serializers import TaskSerializer
from infrastructure.api.serializers.comment_serializers import CommentSerializer
from infrastructure.api.serializers.attachment_serializers import AttachmentSerializer
from infrastructure.di import Container

container = Container()

class TaskViewSet(viewsets.ViewSet):

    def list(self, request):
        tasks = container.tasks.get_task_filters()
        serializer = TaskSerializer(tasks, many=True)
        return Response(serializer.data)

    def retrieve(self, request, pk=None):
        task = container.tasks.get_task_by_id(pk)
        if not task:
            return Response({"detail": "Not found"}, status=status.HTTP_404_NOT_FOUND)
        serializer = TaskSerializer(task)
        return Response(serializer.data)

    def create(self, request):
        data = request.data
        task = container.tasks.create_task(
            project=container.project_repo.get_by_id(data["project_id"]),
            title=data["title"],
            description=data.get("description", ""),
            type=data.get("type", "chore"),
            user=request.user,
            severity=data.get("severity"),
            story_points=data.get("story_points")
        )
        serializer = TaskSerializer(task)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def update(self, request, pk=None):
        task = container.tasks.get_task_by_id(pk)
        if not task:
            return Response({"detail": "Not found"}, status=status.HTTP_404_NOT_FOUND)
        updated_task = container.tasks.update_task(task, **request.data)
        serializer = TaskSerializer(updated_task)
        return Response(serializer.data)

    def destroy(self, request, pk=None):
        container.tasks.delete_task(pk)
        return Response(status=status.HTTP_204_NO_CONTENT)

    @action(detail=True, methods=["post"])
    def add_comment(self, request, pk=None):
        task = container.tasks.get_task_by_id(pk)
        comment = container.tasks.add_comment(task, request.user, request.data["content"])
        serializer = CommentSerializer(comment)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    @action(detail=True, methods=["get"])
    def comments(self, request, pk=None):
        task = container.tasks.get_task_by_id(pk)
        comments = [container.tasks.get_comment_by_id(cid) for cid in task.get_comment_ids()]
        serializer = CommentSerializer(comments, many=True)
        return Response(serializer.data)

    @action(detail=True, methods=["post"])
    def add_attachment(self, request, pk=None):
        task = container.tasks.get_task_by_id(pk)
        file = request.FILES["file"]
        attachment = container.tasks.add_attachment(task, request.user, file)
        serializer = AttachmentSerializer(attachment)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    @action(detail=True, methods=["get"])
    def attachments(self, request, pk=None):
        task = container.tasks.get_task_by_id(pk)
        attachments = [container.tasks.get_attachment_by_id(aid) for aid in task.get_attachment_ids()]
        serializer = AttachmentSerializer(attachments, many=True)
        return Response(serializer.data)
