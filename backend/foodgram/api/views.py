# api/views.py

from rest_framework.viewsets import ReadOnlyModelViewSet

from api.serializers import IngredientSerializer, TagSerializer
from recipes.models import Ingredient, Tag


class TagViewSet(ReadOnlyModelViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer


class IngredientsViewSet(ReadOnlyModelViewSet):
    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializer
