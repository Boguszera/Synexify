# infrastructure/api/views/projects.py

from rest_framework import viewsets, status
from rest_framework.response import Response
from infrastructure.adapters.user_adapter import to_domain_user
from infrastructure.adapters.project_adapter import project_to_dict
from domain.exceptions.exceptions import PermissionDenied
from infrastructure.api.permissions.project_permissions import ProjectPermissions


class ProjectViewSet(viewsets.ViewSet):
    """CRUD Project"""

    def get_container(self):
        from infrastructure.di import Container
        return Container()

    def list(self, request):
        container = self.get_container()
        domain_user = to_domain_user(request.user)
        projects = container.project_service.list_projects(user=domain_user)
        visible_projects = [p for p in projects if ProjectPermissions.can_view(domain_user, p)]
        return Response([project_to_dict(p) for p in visible_projects])

    def retrieve(self, request, pk=None):
        container = self.get_container()
        domain_user = to_domain_user(request.user)
        project = container.project_service.get_project(pk)
        if not project:
            return Response({"detail": "Not found"}, status=404)
        if not ProjectPermissions.can_view(domain_user, project):
            return Response({"detail": "Forbidden"}, status=403)
        return Response(project_to_dict(project))

    def create(self, request):
        container = self.get_container()
        domain_user = to_domain_user(request.user)

        # 1. FAIL FAST: Check if the user is authorized to CREATE the project
        if not ProjectPermissions.can_create(domain_user):
            # We return 403 immediately without relying on service exceptions
            return Response({"detail": "Forbidden: User role cannot create projects"}, status=403)

        try:
            project = container.project_service.create_project(
                name=request.data["name"],
                description=request.data.get("description", ""),
                user=domain_user
            )
            return Response(project_to_dict(project), status=201)
        except PermissionDenied:
            # This catch is now redundant but kept for safety if permissions are re-checked in service
            return Response({"detail": "Forbidden"}, status=403)

    def update(self, request, pk=None):
        container = self.get_container()
        domain_user = to_domain_user(request.user)
        project = container.project_service.get_project(pk)
        if not project:
            return Response({"detail": "Not found"}, status=404)
        try:
            updated = container.project_service.update_project(project, request.data, user=domain_user)
            return Response(project_to_dict(updated))
        except PermissionDenied:
            return Response({"detail": "Forbidden"}, status=403)

    def destroy(self, request, pk=None):
        container = self.get_container()
        domain_user = to_domain_user(request.user)
        project = container.project_service.get_project(pk)
        if not project:
            return Response({"detail": "Not found"}, status=404)
        try:
            container.project_service.delete_project(project, user=domain_user)
            return Response(status=204)
        except PermissionDenied:
            return Response({"detail": "Forbidden"}, status=403)
