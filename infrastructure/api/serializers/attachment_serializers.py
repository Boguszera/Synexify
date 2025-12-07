from rest_framework import serializers

class AttachmentSerializer(serializers.Serializer):
    id = serializers.CharField(read_only=True)
    filename = serializers.CharField()
    uploaded_by_id = serializers.CharField(read_only=True)
    uploaded_at = serializers.DateTimeField(read_only=True)
