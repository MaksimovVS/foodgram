# api/views.py

from rest_framework.viewsets import ReadOnlyModelViewSet, ModelViewSet

from api.serializers import (
    IngredientSerializer,
    RecipeSerializer,
    TagSerializer, ActionRecipeSerializer,
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

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return RecipeSerializer
        return ActionRecipeSerializer

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

    #
    # def perform_update(self, serializer):
    #     ...
