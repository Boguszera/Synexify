# infrastructure/api/serializers/project_serializers.py

from rest_framework import serializers


class ProjectSerializer(serializers.Serializer):
    id = serializers.CharField(read_only=True)
    name = serializers.CharField()
    description = serializers.CharField()
    member_ids = serializers.ListField(child=serializers.CharField(), read_only=True)
    task_ids = serializers.ListField(child=serializers.CharField(), read_only=True)
    sprint_ids = serializers.CharField(required=False, allow_null=True)
    archived = serializers.BooleanField(read_only=True)
