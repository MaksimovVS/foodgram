# users/views.py

from django.contrib.auth import get_user_model
from django.http import HttpResponse
from djoser.views import UserViewSet
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.exceptions import ValidationError
from rest_framework.generics import get_object_or_404
from rest_framework.response import Response

from api.serializers import FollowSerializer
from users.models import Follow
from users.serializers import CustomCreateUserSerializer


User = get_user_model()


class CustomUserViewSet(UserViewSet):
    serializer_class = CustomCreateUserSerializer

    @action(detail=False, methods=('get',))
    def subscriptions(self, request):
        if self.request.user.is_anonymous:
            return Response(status=status.HTTP_401_UNAUTHORIZED)
        pages = self.paginate_queryset(
            User.objects.filter(following__user=request.user)
        )
        serializer = UserFollowingSerializer(pages, many=True)
        return self.get_paginated_response(serializer.data) # падает из-за отсутствия паджинатора

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





        # if request.user.id == int(id):
        #     raise ValidationError('Нельзя подписаться на себя.')
        # author = get_object_or_404(User, id=id)
        # _, status = Follow.objects.get_or_create(user=request.user, author=author)
        # if not status:
        #     raise ValidationError('Вы уже подписаны на данного пользователя.')
        # data = {
        #         'email': author.email,
        #         'id': author.id,
        #         'username': author.username,
        #         'first_name': author.first_name,
        #         'last_name': author.last_name,
        #     }
        # serializer = UserFollowingSerializer(
        #         data=data, context={'request': request})
        # serializer.is_valid()
        # return Response(data=serializer.data,
        #                     status=s.HTTP_201_CREATED)
        # return HttpResponse('привет')
        









        # if request.method == 'POST': # При POST запросе требует JSON разберись
        #     author = get_object_or_404(User, pk=id)
        #     user = self.request.user
        # 
        # 
        #     data = {
        #         'email': author.email,
        #         'id': author.id,
        #         'username': author.username,
        #         'first_name': author.first_name,
        #         'last_name': author.last_name,
        #     }
        #     # data = {'author': author.id, 'user': user.id}
        #     serializer = UserFollowingSerializer(
        #         data=data, context={'request': request}
        #     )
        # 
        # 
        # 
        #     serializer.is_valid(raise_exception=True)
        #     serializer.save()
        #     return Response(data=serializer.data,
        #                     status=status.HTTP_201_CREATED)
        # 
        # author = get_object_or_404(User, pk=id)
        # user = self.request.user
        # subscription = get_object_or_404(
        #     Follow, user=user, author=author
        # )
        # subscription.delete()
        # return Response(status=status.HTTP_204_NO_CONTENT)
