from rest_framework import viewsets, status
from rest_framework.response import Response
from infrastructure.api.serializers.user_serializers import UserSerializer
from infrastructure.di import Container

container = Container()

class UserViewSet(viewsets.ViewSet):
    """CRUD User"""

    def list(self, request):
        users = container.admin_panel.list_users()
        serializer = UserSerializer(users, many=True)
        return Response(serializer.data)

    def retrieve(self, request, pk=None):
        user = container.admin_panel.get_user_by_id(pk)
        if not user:
            return Response({"detail": "Not found"}, status=status.HTTP_404_NOT_FOUND)
        serializer = UserSerializer(user)
        return Response(serializer.data)

    def create(self, request):
        user = container.admin_panel.create_user(
            name=request.data["name"],
            email=request.data["email"],
            role=request.data["role"],
            login=request.data["login"]
        )
        serializer = UserSerializer(user)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def update(self, request, pk=None):
        user = container.admin_panel.get_user_by_id(pk)
        updated_user = container.admin_panel.update_user(user, **request.data)
        serializer = UserSerializer(updated_user)
        return Response(serializer.data)

    def destroy(self, request, pk=None):
        container.admin_panel.delete_user(pk)
        return Response(status=status.HTTP_204_NO_CONTENT)
