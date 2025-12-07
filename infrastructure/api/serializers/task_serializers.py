from rest_framework import serializers
from domain.tasks.task_base import TaskBase

class TaskSerializer(serializers.Serializer):
    id = serializers.CharField(read_only=True)
    title = serializers.CharField()
    description = serializers.CharField()
    status = serializers.CharField()
    project_id = serializers.CharField()
    sprint_id = serializers.IntegerField(allow_null=True)
    assignees_ids = serializers.ListField(child=serializers.CharField(), required=False)
    tag_ids = serializers.ListField(child=serializers.CharField(), required=False)
    comment_ids = serializers.ListField(child=serializers.CharField(), required=False)
    attachment_ids = serializers.ListField(child=serializers.CharField(), required=False)

class TaskCreateUpdateSerializer(serializers.Serializer):
    title = serializers.CharField()
    description = serializers.CharField()
    type = serializers.ChoiceField(choices=['bug', 'feature', 'chore'])
    status = serializers.CharField(required=False)
    assignees_ids = serializers.ListField(child=serializers.CharField(), required=False)
    tag_ids = serializers.ListField(child=serializers.CharField(), required=False)
