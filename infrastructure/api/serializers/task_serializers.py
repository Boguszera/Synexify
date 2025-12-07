from rest_framework import serializers

class TaskSerializer(serializers.Serializer):
    id = serializers.CharField(read_only=True)
    title = serializers.CharField()
    description = serializers.CharField()
    status = serializers.CharField(read_only=True)
    assignee_ids = serializers.ListField(child=serializers.CharField(), read_only=True)
    comment_ids = serializers.ListField(child=serializers.CharField(), read_only=True)
    attachment_ids = serializers.ListField(child=serializers.CharField(), read_only=True)
    tag_ids = serializers.ListField(child=serializers.CharField(), read_only=True)
    project_id = serializers.CharField()
    sprint_id = serializers.IntegerField(required=False, allow_null=True)
