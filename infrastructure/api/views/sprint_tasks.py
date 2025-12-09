from rest_framework import status, viewsets
from rest_framework.response import Response
from infrastructure.adapters.user_adapter import to_domain_user
from domain.exceptions.exceptions import PermissionDenied

class SprintTasksViewSet(viewsets.ViewSet):

    def get_container(self):
        from infrastructure.di import Container
        return Container()

    def list(self, request, sprint_id=None):
        container = self.get_container()
        try:
            domain_user = to_domain_user(request.user)
            sprint = container.sprints.get_by_id(sprint_id)

            if sprint is None:
                return Response({"detail": "Sprint not found"}, status=404)

            container.sprints.check_view_permission(domain_user, sprint)

            tasks = container.tasks.list_by_ids(sprint.get_task_ids())
            serializer = container.task_serializer(tasks, many=True)

            return Response(serializer.data)

        except PermissionDenied as e:
            return Response({"detail": str(e)}, status=403)

    def create(self, request, sprint_id=None):
        container = self.get_container()
        try:
            domain_user = to_domain_user(request.user)

            sprint = container.sprints.get_by_id(sprint_id)
            if sprint is None:
                return Response({"detail": "Sprint not found"}, status=404)

            container.sprints.check_manage_permission(domain_user, sprint)

            task = container.tasks.get_by_id(request.data["task_id"])
            container.sprints.add_task_to_sprint(sprint, task, user=domain_user)

            return Response({"detail": "Task added"}, status=201)

        except PermissionDenied as e:
            return Response({"detail": str(e)}, status=403)

    def destroy(self, request, sprint_id=None, pk=None):
        container = self.get_container()
        try:
            domain_user = to_domain_user(request.user)

            sprint = container.sprints.get_by_id(sprint_id)
            if sprint is None:
                return Response({"detail": "Sprint not found"}, status=404)

            task = container.tasks.get_by_id(pk)

            container.sprints.remove_task_from_sprint(sprint, task, user=domain_user)

            return Response(status=204)

        except PermissionDenied as e:
            return Response({"detail": str(e)}, status=403)
