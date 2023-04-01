# api/views.py

import os

from api.filters import IngredientFilter, TagFilter
from api.paginations import CustomPagination
from api.permissions import IsOwnerOrReadOnly
from api.serializers import (ActionRecipeSerializer, FavoriteRecipeSerializer,
                             IngredientSerializer, RecipeSerializer,
                             TagSerializer)
from django.db.models import Sum
from django.http import FileResponse
from django_filters.rest_framework import DjangoFilterBackend
from recipes.models import Favorite, Ingredient, IngredientRecipe, Recipe, Tag
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.exceptions import ValidationError
from rest_framework.generics import get_object_or_404
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet, ReadOnlyModelViewSet


class TagViewSet(ReadOnlyModelViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    permission_classes = (AllowAny,)


class IngredientViewSet(ReadOnlyModelViewSet):
    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializer
    permission_classes = (AllowAny,)
    filterset_class = IngredientFilter


class RecipeViewSet(ModelViewSet):
    queryset = Recipe.objects.all()
    permission_classes = (IsOwnerOrReadOnly,)
    pagination_class = CustomPagination
    filter_backends = (DjangoFilterBackend,)
    filterset_class = TagFilter

    def get_serializer_class(self):
        if self.request.method == "GET":
            return RecipeSerializer
        return ActionRecipeSerializer

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

    @action(
        detail=True,
        methods=("post", "delete"),
        permission_classes=(IsAuthenticated,),
    )
    def favorite(self, request, pk):
        user = request.user
        if request.method == "DELETE":
            favorite = get_object_or_404(
                Favorite, user=user.id, recipe=pk, is_favorited=True
            )
            favorite.is_favorited = False
            favorite.save()
            return Response(status=status.HTTP_204_NO_CONTENT)
        recipe = get_object_or_404(Recipe, pk=pk)
        favorite, _ = Favorite.objects.get_or_create(user=user, recipe=recipe)
        if favorite.is_favorited:
            raise ValidationError(
                "Нельзя повторно добавить рецепт в избранное."
            )
        favorite.is_favorited = True
        favorite.save()
        serializer = FavoriteRecipeSerializer(recipe)
        return Response(data=serializer.data, status=status.HTTP_201_CREATED)

    @action(
        detail=True,
        methods=("post", "delete"),
        permission_classes=(IsAuthenticated,),
    )
    def shopping_cart(self, request, pk=None):
        user = request.user
        recipe = get_object_or_404(Recipe, pk=pk)
        if request.method == "DELETE":
            shopping_cart = get_object_or_404(
                Favorite, user=user, recipe=recipe, is_in_shopping_cart=True
            )
            shopping_cart.is_in_shopping_cart = False
            shopping_cart.save()
            return Response(status=status.HTTP_204_NO_CONTENT)

        shopping_cart, _ = Favorite.objects.get_or_create(
            user=user,
            recipe=recipe,
        )
        if shopping_cart.is_in_shopping_cart:
            raise ValidationError(
                "Нельзя повторно добавить рецепт в список покупок."
            )
        shopping_cart.is_in_shopping_cart = True
        shopping_cart.save()
        serializer = FavoriteRecipeSerializer(recipe)
        return Response(data=serializer.data, status=status.HTTP_201_CREATED)

    @action(
        detail=False,
        methods=("get",),
        permission_classes=(IsAuthenticated,),
    )
    def download_shopping_cart(self, request):
        ingredients = (
            IngredientRecipe.objects.filter(
                recipe__users_favorites__user=request.user.id
            )
            .values("ingredient__name", "ingredient__measurement_unit")
            .order_by("ingredient__name")
            .annotate(ingredient_total=Sum("amount"))
        )
        filename = "ingredients.txt"
        with open(filename, "w", encoding="utf-8") as f:
            for ingredient in ingredients:
                f.write(
                    f'{ingredient.get("ingredient__name")}: '
                    f'{ingredient.get("ingredient_total")} '
                    f'({ingredient.get("ingredient__measurement_unit")})\n'
                )
        file_path = os.path.join(os.getcwd(), filename)
        return FileResponse(
            open(file_path, "rb"), as_attachment=True, filename=filename
        )
