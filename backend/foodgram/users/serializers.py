# users/serializers.py

from django.contrib.auth import get_user_model
from djoser.serializers import UserSerializer
from rest_framework.serializers import ModelSerializer

User = get_user_model()


class CustomUserSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = (
            'email', 'id', 'username', 'first_name', 'last_name', 'password'
        )
