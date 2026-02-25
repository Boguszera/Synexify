# infrastructure/api/serializers/reporting_serializer.py

from rest_framework import serializers


class ProjectReportSerializer(serializers.Serializer):
    project_id = serializers.CharField()
    project_name = serializers.CharField()
    total_tasks = serializers.IntegerField()
    completed_tasks = serializers.IntegerField()
    overdue_tasks = serializers.IntegerField()
    progress_percentage = serializers.FloatField()


class UserWorkloadSerializer(serializers.Serializer):
    user_id = serializers.CharField()
    user_name = serializers.CharField()
    assigned_tasks = serializers.IntegerField()
    completed_tasks = serializers.IntegerField()
    pending_tasks = serializers.IntegerField()
