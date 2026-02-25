# infrastructure/api/serializers/sprint_serializers.py

from rest_framework import serializers


class SprintSerializer(serializers.Serializer):
    id = serializers.CharField(read_only=True, source="get_id")
    name = serializers.CharField(source="get_name")
    start_date = serializers.DateTimeField(source="get_start_date")
    end_date = serializers.DateTimeField(source="get_end_date")
    project_id = serializers.CharField(source="get_project_id")
    task_ids = serializers.ListField(child=serializers.CharField(), read_only=True, source="get_task_ids")
