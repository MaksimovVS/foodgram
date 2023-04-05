# api/serializers.py

import base64

from django.contrib.auth import get_user_model
from django.core.files.base import ContentFile
from recipes.models import Favorite, Ingredient, IngredientRecipe, Recipe, Tag
from rest_framework import serializers, validators
from users.models import Follow
from users.serializers import CustomUserSerializer

User = get_user_model()


class AddTagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ("id",)


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = "__all__"


class AddIngredientSerializer(serializers.ModelSerializer):
    id = serializers.PrimaryKeyRelatedField(
        queryset=Ingredient.objects.all(),
    )
    amount = serializers.IntegerField()

    class Meta:
        model = IngredientRecipe
        fields = ("id", "amount")


class IngredientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ingredient
        fields = "__all__"


class IngredientAmountSerializer(serializers.ModelSerializer):
    name = serializers.ReadOnlyField(source="ingredient.name")
    measurement_unit = serializers.ReadOnlyField(
        source="ingredient.measurement_unit"
    )

    class Meta:
        model = IngredientRecipe
        fields = ("id", "name", "measurement_unit", "amount")

    validators = (
        validators.UniqueTogetherValidator(
            queryset=IngredientRecipe.objects.all(), fields=(
                "ingredient",
                "recipe",
            )
        ),
    )


class Base64ImageField(serializers.ImageField):
    def to_internal_value(self, data):
        if isinstance(data, str) and data.startswith("data:image"):
            format, imgstr = data.split(";base64,")
            ext = format.split("/")[-1]
            data = ContentFile(base64.b64decode(imgstr), name="temp." + ext)

        return super().to_internal_value(data)


class RecipeSerializer(serializers.ModelSerializer):
    tags = TagSerializer(many=True, read_only=True)
    author = CustomUserSerializer(read_only=True)
    ingredients = IngredientAmountSerializer(
        many=True, read_only=True, source="ingredient_in_recipe"
    )
    is_favorited = serializers.SerializerMethodField()
    is_in_shopping_cart = serializers.SerializerMethodField()
    image = Base64ImageField(required=False, allow_null=True)

    class Meta:
        model = Recipe
        fields = (
            "id",
            "tags",
            "author",
            "ingredients",
            "is_favorited",
            "is_in_shopping_cart",
            "name",
            "image",
            "text",
            "cooking_time",
        )

    def get_is_favorited(self, obj):
        request = self.context.get("request")
        if request is None or request.user.is_anonymous:
            return False
        return Favorite.objects.filter(
            recipe=obj, user=request.user, is_favorited=True
        ).exists()

    def get_is_in_shopping_cart(self, obj):
        request = self.context.get("request")
        if request is None or request.user.is_anonymous:
            return False
        return Favorite.objects.filter(
            recipe=obj, user=request.user, is_in_shopping_cart=True
        ).exists()


class ActionRecipeSerializer(
    serializers.ModelSerializer
):  # поменять на RecipeSerializer?
    tags = serializers.PrimaryKeyRelatedField(
        queryset=Tag.objects.all(),
        many=True,
    )
    ingredients = AddIngredientSerializer(many=True)
    image = Base64ImageField(
        required=False, allow_null=True
    )  # тогда это можно будет удалить

    class Meta:
        model = Recipe
        fields = (
            "ingredients",
            "tags",
            "image",
            "name",
            "text",
            "cooking_time",
        )

    def to_representation(self, instance):
        serializer = RecipeSerializer(instance)
        return serializer.data

    def create(self, validated_data):
        tags = validated_data.pop("tags")
        ingredients = validated_data.pop("ingredients")
        recipe = Recipe.objects.create(**validated_data)
        recipe.tags.set(tags)
        recipe.save()
        for ingredient in ingredients:
            IngredientRecipe.objects.get_or_create(
                recipe=recipe,
                ingredient=ingredient.get("id"),
                amount=ingredient.get("amount"),
            )
        return recipe

    def update(self, instance, validated_data):
        tags = validated_data.pop("tags")
        instance.tags.clear()
        ingredients = validated_data.pop("ingredients")
        instance.ingredients.clear()
        instance.image = validated_data.get("image", instance.image)
        instance.name = validated_data.get("name", instance.name)
        instance.text = validated_data.get("text", instance.text)
        instance.cooking_time = validated_data.get(
            "cooking_time", instance.cooking_time
        )
        instance.tags.set(tags)
        instance.save()
        for ingredient in ingredients:
            IngredientRecipe.objects.get_or_create(
                recipe=instance,
                ingredient=ingredient.get("id"),
                amount=ingredient.get("amount"),
            )
        return instance

    def validate(self, data):
        ingredients = data.get("ingredients")
        if not ingredients:
            raise serializers.ValidationError("Добавьте ингредиенты.")
        for ingredient in ingredients:
            if ingredient.get("amount") <= 0:
                raise serializers.ValidationError(
                    "Количество ингредиентов должно быть больше 0."
                )
        return data


class FavoriteRecipeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Recipe
        fields = (
            "id",
            "name",
            "image",
            "cooking_time",
        )


class FollowSerializer(serializers.ModelSerializer):
    class Meta:
        model = Follow
        fields = ("user", "author")

    def to_representation(self, instance):
        serializer = UserFollowingSerializer(
            User.objects.get(id=instance.author.id),
            context={"request": self.context.get("request")},
        )
        return serializer.data

    def validate(self, data):
        user = data.get("user")
        author = data.get("author")
        if user == author:
            raise serializers.ValidationError(
                "Нельзя подписаться на самого себя."
            )
        if Follow.objects.filter(user=user, author=author).exists():
            raise serializers.ValidationError(
                "Вы уже подписаны на этого пользователя."
            )
        return data


class UserFollowingSerializer(CustomUserSerializer):
    email = serializers.ReadOnlyField()
    id = serializers.ReadOnlyField()
    username = serializers.ReadOnlyField()
    first_name = serializers.ReadOnlyField()
    last_name = serializers.ReadOnlyField()
    is_subscribed = serializers.SerializerMethodField()
    recipes = serializers.SerializerMethodField()
    recipes_count = serializers.SerializerMethodField()

    class Meta:
        model = Follow
        fields = (
            "email",
            "id",
            "username",
            "first_name",
            "last_name",
            "is_subscribed",
            "recipes",
            "recipes_count",
        )

    def get_is_subscribed(self, obj):
        return True

    def get_recipes(self, obj):
        request = self.context.get("request")
        if request.GET.get("recipes_limit"):
            recipe_limit = int(request.GET.get("recipes_limit"))
            queryset = Recipe.objects.filter(author=obj.id)[:recipe_limit]
        else:
            queryset = Recipe.objects.filter(author=obj.id)
        serializer = FavoriteRecipeSerializer(
            queryset,
            read_only=True,
            many=True,
        )
        return serializer.data

    def get_recipes_count(self, obj):
        return obj.recipes.count()
