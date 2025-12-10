# infrastructure/api/serializers/task_serializers.py

from rest_framework import serializers


class TaskSerializer(serializers.Serializer):
    """
    Serializer dla obiektów TaskBase. Używa argumentu 'source',
    aby poprawnie mapować pola na metody dostępowe (gettery) obiektu domenowego.
    """

    # --- Pola podstawowe ---
    id = serializers.CharField(read_only=True, source='get_id')
    title = serializers.CharField(source='get_title')
    description = serializers.CharField(source='get_description')
    status = serializers.CharField(read_only=True, source='get_status')

    # --- Relacje/ID ---
    project_id = serializers.CharField(source='get_project_id')
    # get_sprint_id zwraca Optional[str], więc ustawiamy required=False, allow_null=True
    sprint_id = serializers.CharField(required=False, allow_null=True, source='get_sprint_id')

    # --- Listy ID (odczyt) ---
    # Używamy get_assignees_ids, ponieważ get_assignee_ids zwraca to samo (z TaskBase)
    assignee_ids = serializers.ListField(
        child=serializers.CharField(),
        read_only=True,
        source='get_assignees_ids'
    )
    comment_ids = serializers.ListField(
        child=serializers.CharField(),
        read_only=True,
        source='get_comments_ids'
    )
    attachment_ids = serializers.ListField(
        child=serializers.CharField(),
        read_only=True,
        source='get_attachment_ids'
    )
    tag_ids = serializers.ListField(
        child=serializers.CharField(),
        read_only=True,
        source='get_tag_ids'
    )