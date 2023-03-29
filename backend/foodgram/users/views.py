# users/views.py

from django.contrib.auth import get_user_model
from djoser.views import UserViewSet
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.generics import get_object_or_404
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from api.paginations import CustomPagination
from api.serializers import FollowSerializer, UserFollowingSerializer
from users.models import Follow
from users.serializers import CustomCreateUserSerializer, CustomUserSerializer

User = get_user_model()


class CustomUserViewSet(UserViewSet):
    permission_classes = (IsAuthenticated,)
    pagination_class = CustomPagination

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return CustomUserSerializer
        return CustomCreateUserSerializer

    @action(detail=False, methods=('get',))
    def subscriptions(self, request):
        if self.request.user.is_anonymous:
            return Response(status=status.HTTP_401_UNAUTHORIZED)
        pages = self.paginate_queryset(
            User.objects.filter(following__user=request.user)
        )
        serializer = UserFollowingSerializer(
            pages,
            many=True,
            context={'request': request}
        )
        return self.get_paginated_response(
            serializer.data)

    @action(detail=True, methods=('post', 'delete'))
    def subscribe(self, request, id):
        author = get_object_or_404(User, id=id)
        user = self.request.user
        if request.method == 'DELETE':
            follow = get_object_or_404(
                Follow, user=user, author=author
            )
            follow.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)

        data = {'author': author.id, 'user': user.id}
        serializer = FollowSerializer(
            data=data, context={'request': request}
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(data=serializer.data, status=status.HTTP_201_CREATED)
