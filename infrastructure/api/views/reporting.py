# infrastructure/api/views/reporting.py

from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from infrastructure.api.serializers.attachment_serializers import AttachmentSerializer
from infrastructure.api.serializers.reporting_serializers import ProjectReportSerializer, UserWorkloadSerializer


class AttachmentDetailView(APIView):
    def get_container(self):
        from infrastructure.di import Container

        return Container()

    def get(self, request, attachment_id):
        container = self.get_container()
        attachment_repo = container.task_repo
        attachment = attachment_repo.get_attachment_by_id(attachment_id)  # trzeba dodać metodę repo
        if not attachment:
            return Response({"detail": "Not found"}, status=status.HTTP_404_NOT_FOUND)
        serializer = AttachmentSerializer(attachment)
        return Response(serializer.data)


class ProjectReportView(APIView):
    def get(self, request, project_id):
        container = self.get_container()
        report_service = container.reporting
        report_data = report_service.project_progress(project_id)
        serializer = ProjectReportSerializer(report_data)
        return Response(serializer.data)


class TeamWorkloadView(APIView):
    def get(self, request, project_id):
        container = self.get_container()
        report_service = container.reporting
        workload = report_service.team_workload(project_id)
        serializer = UserWorkloadSerializer(workload, many=True)
        return Response(serializer.data)


class DashboardView(APIView):
    def get(self, request):
        return Response({"message": "Dashboard not implemented yet"})
