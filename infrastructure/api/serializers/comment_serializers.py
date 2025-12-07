from rest_framework import serializers

class CommentSerializer(serializers.Serializer):
    id = serializers.CharField(read_only=True)
    content = serializers.CharField()
    author_id = serializers.CharField(read_only=True)
    created_at = serializers.DateTimeField(read_only=True)
