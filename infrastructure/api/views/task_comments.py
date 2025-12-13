# infrastructure/api/views/task_comments.py
from rest_framework import viewsets, status
from rest_framework.response import Response
from infrastructure.di import Container
from infrastructure.adapters.user_adapter import to_domain_user
from infrastructure.api.serializers.comment_serializers import CommentSerializer
from domain.exceptions.exceptions import PermissionDenied
from infrastructure.api.permissions.project_permissions import ProjectPermissions

class CommentViewSet(viewsets.ViewSet):
    def get_container(self):
        from infrastructure.di import Container
        return Container()

    def _check_task_access(self, container, user, task_id):
        task = container.tasks.task_repo.get_by_id(task_id)
        if not task:
            return None, Response({"detail": "Task not found"}, status=status.HTTP_404_NOT_FOUND)

        project = container.project_service.get_project(task.get_project_id())
        if not project:
            return None, Response({"detail": "Project not found"}, status=status.HTTP_404_NOT_FOUND)

        if not ProjectPermissions.can_view(user, project):
            return None, Response({"detail": "Forbidden"}, status=status.HTTP_403_FORBIDDEN)

        return task, None

    def list(self, request, task_pk=None):
        container = self.get_container()
        domain_user = to_domain_user(request.user)

        _, error = self._check_task_access(container, domain_user, task_pk)
        if error: return error

        comments = container.comments.list_comments_for_task(task_pk, domain_user)
        return Response(CommentSerializer(comments, many=True).data)

    def create(self, request, task_pk=None):
        container = self.get_container()
        domain_user = to_domain_user(request.user)

        _, error = self._check_task_access(container, domain_user, task_pk)
        if error: return error

        try:
            comment = container.comments.add_comment(task_pk, domain_user, request.data.get("content", ""))
            return Response(CommentSerializer(comment).data, status=status.HTTP_201_CREATED)
        except (PermissionDenied, ValueError) as e:
            return Response({"detail": str(e)}, status=status.HTTP_400_BAD_REQUEST)