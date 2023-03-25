# api/views.py

from rest_framework.viewsets import ReadOnlyModelViewSet, ModelViewSet

from api.serializers import (
    IngredientSerializer,
    RecipeSerializer,
    TagSerializer,
)

from recipes.models import Ingredient, Tag, Recipe


class TagViewSet(ReadOnlyModelViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer


class IngredientViewSet(ReadOnlyModelViewSet):
    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializer


class RecipeViewSet(ModelViewSet):
    queryset = Recipe.objects.all()
    serializer_class = RecipeSerializer
