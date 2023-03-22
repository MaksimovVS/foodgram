# users/views.py

from djoser.views import UserViewSet

from users.serializers import CustomCreateUserSerializer


class CustomUserViewSet(UserViewSet):
    serializer_class = CustomCreateUserSerializer
