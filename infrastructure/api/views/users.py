# infrastructure/api/views/users.py
from rest_framework import viewsets, status
from rest_framework.response import Response
from infrastructure.api.serializers.user_serializers import UserSerializer
from infrastructure.adapters.user_adapter import to_domain_user
from domain.exceptions.exceptions import PermissionDenied

class UserViewSet(viewsets.ViewSet):
    def get_container(self):
        from infrastructure.di import Container
        return Container()

    def list(self, request):
        container = self.get_container()
        try:
            domain_user = to_domain_user(request.user)
            users = container.admin_panel.list_users(user=domain_user)
            serializer = UserSerializer(users, many=True)
            return Response(serializer.data)
        except PermissionDenied as e:
            return Response({"detail": str(e)}, status=status.HTTP_403_FORBIDDEN)

    def retrieve(self, request, pk=None):
        container = self.get_container()
        try:
            domain_user = to_domain_user(request.user)
            user = container.admin_panel.get_user_by_id(pk)
            if not user:
                return Response({"detail": "Not found"}, status=status.HTTP_404_NOT_FOUND)
            serializer = UserSerializer(user)
            return Response(serializer.data)
        except PermissionDenied as e:
            return Response({"detail": str(e)}, status=status.HTTP_403_FORBIDDEN)

    def create(self, request):
        container = self.get_container()
        try:
            domain_user = to_domain_user(request.user)
            user = container.admin_panel.create_user(
                name=request.data["name"],
                email=request.data["email"],
                role=request.data["role"],
                login=request.data["login"],
                user=domain_user
            )
            serializer = UserSerializer(user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        except PermissionDenied as e:
            return Response({"detail": str(e)}, status=status.HTTP_403_FORBIDDEN)

    def update(self, request, pk=None):
        container = self.get_container()
        try:
            domain_user = to_domain_user(request.user)
            target_user = container.admin_panel.get_user_by_id(pk)
            updated_user = container.admin_panel.update_user(target_user, request.data, user=domain_user)
            serializer = UserSerializer(updated_user)
            return Response(serializer.data)
        except PermissionDenied as e:
            return Response({"detail": str(e)}, status=status.HTTP_403_FORBIDDEN)

    def destroy(self, request, pk=None):
        container = self.get_container()
        try:
            domain_user = to_domain_user(request.user)
            target_user = container.admin_panel.get_user_by_id(pk)
            container.admin_panel.delete_user(target_user, user=domain_user)
            return Response(status=status.HTTP_204_NO_CONTENT)
        except PermissionDenied as e:
            return Response({"detail": str(e)}, status=status.HTTP_403_FORBIDDEN)
