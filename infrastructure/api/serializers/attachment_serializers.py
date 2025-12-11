# infrastructure/api/serializers/attachment_serializers.py

from rest_framework import serializers

class AttachmentSerializer(serializers.Serializer):
    id = serializers.CharField(read_only=True, source='get_id')
    filename = serializers.CharField(read_only=True, source='get_filename')
    uploaded_by_id = serializers.CharField(read_only=True, source='get_uploaded_by_id')
    uploaded_at = serializers.DateTimeField(read_only=True, source='get_uploaded_at')