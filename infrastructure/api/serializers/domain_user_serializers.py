# infrastructure/api/serializers/domain_user_serializers.py
from rest_framework import serializers

class DomainUserSerializer(serializers.Serializer):
    # infrastructure/api/serializers/domain_user_serializers.py
    from rest_framework import serializers

    class DomainUserSerializer(serializers.Serializer):
        id = serializers.CharField(source='get_id', read_only=True)
        name = serializers.CharField(source='get_name')
        email = serializers.EmailField(source='get_email')
        role = serializers.CharField(source='get_role')
        login = serializers.CharField(source='get_login')