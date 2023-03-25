# api/serializers.py

from rest_framework import serializers

from recipes.models import Ingredient, Recipe, Tag
from users.serializers import CustomUserSerializer


class TagSerializer(serializers.ModelSerializer):

    class Meta:
        model = Tag
        fields = '__all__'


class IngredientSerializer(serializers.ModelSerializer):

    class Meta:
        model = Ingredient
        fields = '__all__'

    def to_representation(self, instance):
        """Convert `username` to lowercase."""
        a = instance
        print(a)
        # ret = super().to_representation(instance)
        # ret['username'] = ret['username'].lower()
        return None


class RecipeSerializer(serializers.ModelSerializer):
    tags = TagSerializer(many=True, read_only=True)
    author = CustomUserSerializer(read_only=True)
    ingredients = IngredientSerializer(many=True, read_only=True)

    class Meta:
        model = Recipe
        # fields = '__all__'
        fields = ('id', 'tags', 'author', 'ingredients', 'name', 'image', 'text', 'cooking_time')

    # def to_representation(self, instance):
    #     data = super(IngredientSerializer, self).to_representation(instance)
    #     # data['amount'] = instance.job_result.user.username
    #     a = instance
    #     print(a)
    #     return data
    # def to_representation(self, instance):
    #     """Convert `username` to lowercase."""
    #     a = instance
    #     print(a)
    #     # ret = super().to_representation(instance)
    #     # ret['username'] = ret['username'].lower()
    #     return None