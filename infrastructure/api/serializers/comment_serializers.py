# infrastructure/api/serializers/comment_serializers.py

from rest_framework import serializers


class CommentSerializer(serializers.Serializer):
    id = serializers.CharField(read_only=True, source="get_id")
    content = serializers.CharField(source="get_content")
    author_id = serializers.CharField(read_only=True, source="get_author_id")
    created_at = serializers.DateTimeField(read_only=True, source="get_created_at")
