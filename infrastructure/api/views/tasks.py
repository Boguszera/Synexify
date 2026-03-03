# infrastructure/api/views/tasks.py
from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from domain.exceptions.exceptions import PermissionDenied
from infrastructure.adapters.user_adapter import to_domain_user
from infrastructure.api.serializers.attachment_serializers import AttachmentSerializer
from infrastructure.api.serializers.comment_serializers import CommentSerializer
from infrastructure.api.serializers.task_serializers import TaskSerializer


class TaskViewSet(viewsets.ViewSet):
    def get_container(self):
        from infrastructure.di import Container

        return Container()

    def list(self, request):
        container = self.get_container()
        try:
            domain_user = to_domain_user(request.user)
            filters = {}

            if "status" in request.query_params:
                filters["status"] = request.query_params["status"]

            tasks = container.tasks.get_task_filters(user=domain_user, **filters)
            serializer = TaskSerializer(tasks, many=True)
            return Response(serializer.data)
        except PermissionDenied as e:
            return Response({"detail": str(e)}, status=status.HTTP_403_FORBIDDEN)

    def retrieve(self, request, pk=None):
        container = self.get_container()
        try:
            task = container.tasks.task_repo.get_by_id(pk)
            if not task:
                return Response({"detail": "Not found"}, status=status.HTTP_404_NOT_FOUND)
            serializer = TaskSerializer(task)
            return Response(serializer.data)
        except PermissionDenied as e:
            return Response({"detail": str(e)}, status=status.HTTP_403_FORBIDDEN)

    def create(self, request):
        container = self.get_container()
        try:
            domain_user = to_domain_user(request.user)
            data = request.data
            task = container.tasks.create_task(
                project=container.project_repo.get_by_id(data["project_id"]),
                title=data["title"],
                description=data.get("description", ""),
                task_type=data.get("type", "chore"),
                user=domain_user,
                severity=data.get("severity"),
                story_points=data.get("story_points"),
            )
            serializer = TaskSerializer(task)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        except PermissionDenied as e:
            return Response({"detail": str(e)}, status=status.HTTP_403_FORBIDDEN)

    def partial_update(self, request, pk=None):
        container = self.get_container()
        try:
            domain_user = to_domain_user(request.user)
            task = container.tasks.task_repo.get_by_id(pk)
            if not task:
                return Response({"detail": "Not found"}, status=status.HTTP_404_NOT_FOUND)
            updated_task = container.tasks.update_task(task, user=domain_user, **request.data)
            serializer = TaskSerializer(updated_task)
            return Response(serializer.data)
        except PermissionDenied as e:
            return Response({"detail": str(e)}, status=status.HTTP_403_FORBIDDEN)
        except ValueError as e:
            return Response({"detail": str(e)}, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, pk=None):
        container = self.get_container()
        try:
            domain_user = to_domain_user(request.user)
            container.tasks.delete_task(pk, user=domain_user)
            return Response(status=status.HTTP_204_NO_CONTENT)
        except PermissionDenied as e:
            return Response({"detail": str(e)}, status=status.HTTP_403_FORBIDDEN)

    @action(detail=True, methods=["post"])
    def add_comment(self, request, pk=None):
        container = self.get_container()
        try:
            domain_user = to_domain_user(request.user)
            task = container.tasks.task_repo.get_by_id(pk)
            comment = container.tasks.add_comment(task, domain_user, request.data["content"])
            serializer = CommentSerializer(comment)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        except PermissionDenied as e:
            return Response({"detail": str(e)}, status=status.HTTP_403_FORBIDDEN)

    @action(detail=True, methods=["get"])
    def comments(self, request, pk=None):
        container = self.get_container()
        domain_user = to_domain_user(request.user)
        task = container.tasks.task_repo.get_by_id(pk)

        if not task:
            return Response({"detail": "Task not found"}, status=status.HTTP_404_NOT_FOUND)

        project = container.project_service.get_project(task.get_project_id())
        if not project or not container.auth.can_view_project(domain_user, project):
            return Response({"detail": "Forbidden"}, status=status.HTTP_403_FORBIDDEN)

        comments = container.comments.list_comments_for_task(pk, domain_user)
        serializer = CommentSerializer(comments, many=True)
        return Response(serializer.data)

    @action(detail=True, methods=["post"])
    def add_attachment(self, request, pk=None):
        container = self.get_container()
        try:
            domain_user = to_domain_user(request.user)
            task = container.tasks.task_repo.get_by_id(pk)
            file = request.FILES["file"]
            attachment = container.attachments.add_attachment(task_id=task.get_id(), user=domain_user, file=file)
            serializer = AttachmentSerializer(attachment)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        except PermissionDenied as e:
            return Response({"detail": str(e)}, status=status.HTTP_403_FORBIDDEN)
        except Exception as e:
            print(f"FATAL UPLOAD ERROR: {type(e).__name__} - {e}")
            return Response(
                {"detail": f"Internal Server Error during upload: {type(e).__name__}"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )

    @action(detail=True, methods=["get"])
    def attachments(self, request, pk=None):
        container = self.get_container()
        task = container.tasks.task_repo.get_by_id(pk)
        if not task:
            return Response({"detail": "Task not found"}, status=status.HTTP_404_NOT_FOUND)
        attachments = [container.tasks.get_attachment_by_id(aid) for aid in task.get_attachment_ids()]
        serializer = AttachmentSerializer(attachments, many=True)
        return Response(serializer.data)

    @action(detail=True, methods=["patch"])
    def assign(self, request, pk=None):
        container = self.get_container()
        domain_user = to_domain_user(request.user)

        task = container.tasks.task_repo.get_by_id(pk)
        if not task:
            return Response({"detail": "Task not found"}, status=status.HTTP_404_NOT_FOUND)

        assignee_id = request.data.get("assignee_id")
        if not assignee_id:
            return Response({"detail": "assignee_id is required"}, status=status.HTTP_400_BAD_REQUEST)

        try:
            container.tasks.assign_task_by_id(task, domain_user, assignee_id)
            return Response({"status": f"Task assigned to {assignee_id}"}, status=status.HTTP_200_OK)

        except PermissionDenied as e:
            return Response({"detail": str(e)}, status=status.HTTP_403_FORBIDDEN)
        except ValueError as e:
            return Response({"detail": str(e)}, status=status.HTTP_400_BAD_REQUEST)
