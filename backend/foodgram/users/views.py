# users/views.py

from django.contrib.auth import get_user_model
from django.http import HttpResponse
from djoser.views import UserViewSet
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.response import Response

from api.serializers import UserFollowingSerializer
from users.serializers import CustomCreateUserSerializer


User = get_user_model()


class CustomUserViewSet(UserViewSet):
    serializer_class = CustomCreateUserSerializer

    @action(detail=False, methods=('get',))
    def subscriptions(self, request):
        # followers = User.objects.filter(following__user=request.user)
        #
        # serializer = CustomUserSerializer(list(followers), many=True)
        # return Response(serializer.data)

        if self.request.user.is_anonymous:
            return Response(status=status.HTTP_401_UNAUTHORIZED)
        pages = self.paginate_queryset(
            User.objects.filter(following__user=request.user)
        )
        serializer = UserFollowingSerializer(pages, many=True)
        return self.get_paginated_response(serializer.data) # падает из-за отсутствия паджинатора
        return HttpResponse('Привет')
