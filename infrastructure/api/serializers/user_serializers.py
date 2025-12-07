# infrastructure/api/serializers/user_serializers.py

from rest_framework import serializers

class UserSerializer(serializers.Serializer):
    id = serializers.CharField(read_only=True)
    name = serializers.CharField()
    email = serializers.EmailField()
    role = serializers.CharField()
    login = serializers.CharField()
