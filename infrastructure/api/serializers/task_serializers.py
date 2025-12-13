# infrastructure/api/serializers/task_serializers.py

from rest_framework import serializers


class TaskSerializer(serializers.Serializer):
    # ... (Pola id, title, description, status, project_id, sprint_id bez zmian) ...
    id = serializers.CharField(read_only=True, source='get_id')
    title = serializers.CharField(source='get_title')
    description = serializers.CharField(source='get_description')
    status = serializers.CharField(read_only=True, source='get_status')

    project_id = serializers.CharField(source='get_project_id')
    sprint_id = serializers.CharField(required=False, allow_null=True, source='get_sprint_id')

    # [FIX C] Dodajemy pola specyficzne dla typów zadań z bezpiecznym SerializerMethodField

    task_type = serializers.CharField(source='get_task_type', read_only=True)  # Załóżmy, że TaskBase ma get_task_type()

    severity = serializers.SerializerMethodField(read_only=True)
    story_points = serializers.SerializerMethodField(read_only=True)

    def get_severity(self, obj):
        return getattr(obj, 'get_severity', lambda: None)()

    def get_story_points(self, obj):
        return getattr(obj, 'get_story_points', lambda: None)()
