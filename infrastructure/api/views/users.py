# infrastructure/api/views/users.py
from rest_framework import viewsets, mixins, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, BasePermission
from infrastructure.adapters.user_adapter import to_domain_user, to_dict
from domain.exceptions.exceptions import PermissionDenied

class IsAdminUser(BasePermission):
    def has_permission(self, request, view):
        return (
            request.user
            and request.user.is_authenticated
            and getattr(request.user, "role", None) == "admin"
        )

class UserViewSet(
    mixins.ListModelMixin,
    mixins.RetrieveModelMixin,
    mixins.CreateModelMixin,
    mixins.UpdateModelMixin,
    mixins.DestroyModelMixin,
    viewsets.GenericViewSet
):
    permission_classes = [IsAuthenticated, IsAdminUser]

    def get_container(self):
        from infrastructure.di import Container
        return Container()

    def list(self, request, *args, **kwargs):
        container = self.get_container()
        domain_user = to_domain_user(request.user)
        try:
            users = container.admin_panel.list_users(user=domain_user)
            return Response([to_dict(u) for u in users])
        except PermissionDenied as e:
            return Response({"detail": str(e)}, status=status.HTTP_403_FORBIDDEN)

    def retrieve(self, request, pk=None, *args, **kwargs):
        container = self.get_container()
        domain_user = to_domain_user(request.user)
        try:
            user = container.admin_panel.get_user_by_id(pk)
            if not user:
                return Response({"detail": "Not found"}, status=status.HTTP_404_NOT_FOUND)
            return Response(to_dict(user))
        except PermissionDenied as e:
            return Response({"detail": str(e)}, status=status.HTTP_403_FORBIDDEN)

    def create(self, request, *args, **kwargs):
        container = self.get_container()
        domain_user = to_domain_user(request.user)

        try:
            created = container.admin_panel.create_user(
                name=request.data.get("name"),
                email=request.data.get("email"),
                role=request.data.get("role"),
                login=request.data.get("login"),
                password=request.data.get("password"),
                user=domain_user
            )

            return Response(to_dict(created), status=status.HTTP_201_CREATED)

        except PermissionDenied as e:
            return Response({"detail": str(e)}, status=status.HTTP_403_FORBIDDEN)

    def update(self, request, pk=None, *args, **kwargs):
        container = self.get_container()
        domain_user = to_domain_user(request.user)
        try:
            target_user = container.admin_panel.get_user_by_id(pk)
            if not target_user:
                return Response({"detail": "Not found"}, status=status.HTTP_404_NOT_FOUND)
            updated_user = container.admin_panel.update_user(
                user_id=pk,
                fields=request.data,
                user=domain_user
            )
            return Response(to_dict(updated_user))
        except PermissionDenied as e:
            return Response({"detail": str(e)}, status=status.HTTP_403_FORBIDDEN)

    def destroy(self, request, *args, **kwargs):
        container = self.get_container()
        domain_user = to_domain_user(request.user)
        user_id = kwargs.get("pk")
        target_user = container.admin_panel.get_user_by_id(user_id)

        if not target_user:
            return Response({"detail": "Not found"}, status=404)

        try:
            container.admin_panel.delete_user(user_id, user=domain_user)
            return Response(status=204)
        except PermissionDenied as e:
            return Response({"detail": str(e)}, status=403)
