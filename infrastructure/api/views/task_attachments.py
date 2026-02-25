from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from infrastructure.adapters.user_adapter import to_domain_user
from infrastructure.api.permissions.project_permissions import ProjectPermissions
from infrastructure.api.serializers.attachment_serializers import AttachmentSerializer
from infrastructure.di import Container


# infrastructure/api/views/task_attachments.py
class AttachmentViewSet(viewsets.ViewSet):
    def get_container(self):
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
        if error:
            return error

        attachments = container.attachments.list_attachments_for_task(task_pk, domain_user)
        return Response(AttachmentSerializer(attachments, many=True).data)

    def create(self, request, task_pk=None):
        container = self.get_container()
        domain_user = to_domain_user(request.user)
        _, error = self._check_task_access(container, domain_user, task_pk)
        if error:
            return error

        if "file" not in request.FILES:
            return Response({"detail": "File required"}, status=400)

        try:
            attachment = container.attachments.add_attachment(task_pk, domain_user, request.FILES["file"])
            return Response(AttachmentSerializer(attachment).data, status=201)
        except Exception as e:
            return Response({"detail": str(e)}, status=400)

    @action(detail=True, methods=["get"])
    def download(self, request, task_pk=None, pk=None):
        container = self.get_container()
        domain_user = to_domain_user(request.user)
        _, error = self._check_task_access(container, domain_user, task_pk)
        if error:
            return error

        try:
            content = container.attachments.download_attachment(pk, domain_user)
            return Response(content, content_type="application/octet-stream")
        except Exception as e:
            return Response({"detail": str(e)}, status=404)
