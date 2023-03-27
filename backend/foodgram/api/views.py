# api/views.py
import os

from django.db.models import Sum
from django.http import FileResponse
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.exceptions import ValidationError
from rest_framework.generics import get_object_or_404
from rest_framework.response import Response
from rest_framework.viewsets import ReadOnlyModelViewSet, ModelViewSet

from api.serializers import (
    IngredientSerializer,
    RecipeSerializer,
    TagSerializer, ActionRecipeSerializer, FavoriteRecipeSerializer,
)

from recipes.models import Ingredient, Tag, Recipe, Favorite, IngredientRecipe


class TagViewSet(ReadOnlyModelViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer


class IngredientViewSet(ReadOnlyModelViewSet):
    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializer


class RecipeViewSet(ModelViewSet):
    queryset = Recipe.objects.all()

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return RecipeSerializer
        return ActionRecipeSerializer

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

    #
    # def perform_update(self, serializer):
    #     ...

    @action(detail=True, methods=('post', 'delete'))
    def favorite(self, request, pk=None):
        user = request.user
        if request.method == 'DELETE':
            favorite = get_object_or_404(Favorite, user=user.id, recipe=pk, is_favorited=True)
            favorite.is_favorited = False
            favorite.save()
            return Response(status=status.HTTP_204_NO_CONTENT)
        recipe = get_object_or_404(Recipe, pk=pk)
        favorite, _ = Favorite.objects.get_or_create(user=user.id, recipe=pk)
        if favorite.is_favorited:
            raise ValidationError('Нельзя повторно добавить рецепт в избранное.')
        favorite.is_favorited = True
        favorite.save()
        serializer = FavoriteRecipeSerializer(recipe)
        return Response(data=serializer.data, status=status.HTTP_201_CREATED)

    @action(detail=True, methods=('post', 'delete'))
    def shopping_cart(self, request, pk=None):
        user = request.user
        if request.method == 'DELETE':
            shopping_cart = get_object_or_404(Favorite, user=user.id, recipe=pk,
                                         is_in_shopping_cart=True)
            shopping_cart.is_in_shopping_cart = False
            shopping_cart.save()
            return Response(status=status.HTTP_204_NO_CONTENT)
        recipe = get_object_or_404(Recipe, pk=pk)
        shopping_cart, _ = Favorite.objects.get_or_create(user=user.id, recipe=recipe)
        if shopping_cart.is_in_shopping_cart:
            raise ValidationError('Нельзя повторно добавить рецепт в список покупок.')
        shopping_cart.is_in_shopping_cart = True
        shopping_cart.save()
        serializer = FavoriteRecipeSerializer(recipe)
        return Response(data=serializer.data, status=status.HTTP_201_CREATED)

    @action(detail=False, methods=('get',))
    def download_shopping_cart(self, request):
        ingredients = IngredientRecipe.objects.filter(
            recipe__favorite__user=request.user.id
        ).values(
            'ingredient__name', 'ingredient__measurement_unit'
        ).order_by(
            'ingredient__name'
        ).annotate(ingredient_total=Sum('amount'))
        filename = 'ingredients.txt'
        with open(filename, 'w', encoding='utf-8') as f:
            for ingredient in ingredients:
                f.write(f'{ingredient.get("ingredient__name")}: {ingredient.get("ingredient_total")} ({ingredient.get("ingredient__measurement_unit")})\n')
        file_path = os.path.join(os.getcwd(), filename)
        file_response = FileResponse(open(file_path, 'rb'), as_attachment=True, filename=filename)
        return file_response
