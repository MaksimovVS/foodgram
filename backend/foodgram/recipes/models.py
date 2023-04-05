# recipes/models.py

from django.contrib.auth import get_user_model
from django.core.validators import MinValueValidator
from django.db import models
from django.utils.translation import gettext_lazy as _

MIN_VALUE_IN_FIELD = 1

User = get_user_model()


class Tag(models.Model):
    name = models.CharField(
        _("Название тега"),
        max_length=200,
    )
    color = models.CharField(max_length=7)
    slug = models.SlugField(
        _("slug Тега"),
        max_length=200,
        unique=True,
    )

    class Meta:
        verbose_name = "Тег"
        verbose_name_plural = "Теги"

    def __str__(self):
        return self.name


class Ingredient(models.Model):
    name = models.CharField(
        _("Название ингредиента"),
        max_length=200,
    )
    measurement_unit = models.CharField(
        _("Единица измерения"),
        max_length=200,
    )

    class Meta:
        verbose_name = "Ингредиент"
        verbose_name_plural = "Ингредиенты"

    def __str__(self):
        return self.name


class Recipe(models.Model):
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="recipes",
        verbose_name="Автор",
    )
    name = models.CharField(
        _("Название рецепта"),
        max_length=128,
    )
    image = models.ImageField(
        _("Картинка"),
        upload_to="recipes/images/",
        blank=True,
    )
    text = models.TextField(
        _("Описание рецепта"),
    )
    cooking_time = models.PositiveIntegerField(validators=(
        MinValueValidator(
            MIN_VALUE_IN_FIELD,
            message='Количество должно быть не меньше 1'
        ),
    ))
    tags = models.ManyToManyField(Tag, through="TagRecipe")
    ingredients = models.ManyToManyField(
        Ingredient,
        through="IngredientRecipe",
    )
    pub_date = models.DateTimeField(
        _("Дата публикации"),
        auto_now_add=True,
    )

    class Meta:
        verbose_name = "Рецепт"
        verbose_name_plural = "Рецепты"
        ordering = ("-pub_date",)

    def __str__(self):
        return self.name


class TagRecipe(models.Model):
    tag = models.ForeignKey(Tag, on_delete=models.CASCADE)
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE)

    class Meta:
        verbose_name = "Тег"
        verbose_name_plural = "Теги"

    def __str__(self):
        return f"{self.tag} {self.recipe}"


class IngredientRecipe(models.Model):
    ingredient = models.ForeignKey(Ingredient, on_delete=models.CASCADE)
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        related_name="ingredient_in_recipe",
    )
    amount = models.PositiveIntegerField(validators=(
        MinValueValidator(
            MIN_VALUE_IN_FIELD,
            message='Количество должно быть не меньше 1'
        ),
    ))

    # validators = (
    #     MinValueValidator(
    #         Limits.MIN_AMOUNT_INGREDIENTS,
    #         'Нужно хоть какое-то количество.',
    #     ),


    class Meta:
        constraints = (
            models.UniqueConstraint(
                fields=("ingredient", "recipe"), name="unique_ingredient"
            ),
        )
        verbose_name = "Ингредиенты рецепта"
        verbose_name_plural = "Ингредиенты рецептов"

    def __str__(self):
        return f"{self.ingredient} {self.recipe}"


class Favorite(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="favorite",
    )
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        related_name="users_favorites",
    )
    is_favorited = models.BooleanField(null=True)
    is_in_shopping_cart = models.BooleanField(null=True)

    class Meta:
        constraints = (
            models.UniqueConstraint(
                fields=("user", "recipe"),
                name="unique_favorite"
            ),
        )
        verbose_name = "Избранное"
        verbose_name_plural = "Избранное"

    def __str__(self):
        return f"{self.user} добавил в избранное {self.recipe}"
