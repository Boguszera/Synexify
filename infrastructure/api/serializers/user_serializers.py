# infrastructure/api/serializers/user_serializers
from rest_framework import status, viewsets
from rest_framework.permissions import BasePermission, IsAuthenticated
from rest_framework.response import Response

from domain.exceptions.exceptions import PermissionDenied
from infrastructure.adapters.user_adapter import to_domain_user
from infrastructure.api.serializers.domain_user_serializers import DomainUserSerializer


class IsAdminUser(BasePermission):
    def has_permission(self, request, view):
        return request.user and request.user.is_authenticated and getattr(request.user, "role", None) == "admin"


class UserViewSet(viewsets.ViewSet):
    permission_classes = [IsAuthenticated, IsAdminUser]

    def get_container(self):
        from infrastructure.di import Container

        return Container()

    def list(self, request):
        container = self.get_container()
        domain_user = to_domain_user(request.user)
        try:
            users = container.admin_panel.list_users(user=domain_user)
            serializer = DomainUserSerializer(users, many=True)
            return Response(serializer.data)
        except PermissionDenied as e:
            return Response({"detail": str(e)}, status=status.HTTP_403_FORBIDDEN)

    def retrieve(self, request, pk=None):
        container = self.get_container()
        try:
            user = container.admin_panel.get_user_by_id(pk)
            if not user:
                return Response({"detail": "Not found"}, status=status.HTTP_404_NOT_FOUND)
            serializer = DomainUserSerializer(user)
            return Response(serializer.data)
        except PermissionDenied as e:
            return Response({"detail": str(e)}, status=status.HTTP_403_FORBIDDEN)

    def create(self, request):
        container = self.get_container()
        domain_user = to_domain_user(request.user)
        try:
            user = container.admin_panel.create_user(
                name=request.data.get("name"),
                email=request.data.get("email"),
                role=request.data.get("role"),
                login=request.data.get("login"),
                user=domain_user,
            )
            serializer = DomainUserSerializer(user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        except PermissionDenied as e:
            return Response({"detail": str(e)}, status=status.HTTP_403_FORBIDDEN)

    def update(self, request, pk=None):
        container = self.get_container()
        domain_user = to_domain_user(request.user)
        try:
            target_user = container.admin_panel.get_user_by_id(pk)
            if not target_user:
                return Response({"detail": "Not found"}, status=status.HTTP_404_NOT_FOUND)
            updated_user = container.admin_panel.update_user(target_user, request.data, user=domain_user)
            serializer = DomainUserSerializer(updated_user)
            return Response(serializer.data)
        except PermissionDenied as e:
            return Response({"detail": str(e)}, status=status.HTTP_403_FORBIDDEN)

    def destroy(self, request, pk=None):
        container = self.get_container()
        domain_user = to_domain_user(request.user)
        try:
            target_user = container.admin_panel.get_user_by_id(pk)
            if not target_user:
                return Response({"detail": "Not found"}, status=status.HTTP_404_NOT_FOUND)
            container.admin_panel.delete_user(target_user, user=domain_user)
            return Response(status=status.HTTP_204_NO_CONTENT)
        except PermissionDenied as e:
            return Response({"detail": str(e)}, status=status.HTTP_403_FORBIDDEN)
