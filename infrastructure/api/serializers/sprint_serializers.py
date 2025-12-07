# infrastructure/api/serializers/sprint_serializers.py

from rest_framework import serializers

class SprintSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    name = serializers.CharField()
    start_date = serializers.DateField()
    end_date = serializers.DateField()
    project_id = serializers.CharField()
    task_ids = serializers.ListField(child=serializers.CharField(), read_only=True)
