# recipes/models.py

from django.contrib.auth import get_user_model
from django.db import models

User = get_user_model()


class Tag(models.Model):
    name = models.CharField(
        'Название тега',
        max_length=200,
    )
    color = models.CharField(max_length=7)
    slug = models.SlugField(
        'slug Тега',
        max_length=200,
        unique=True,
    )

    class Meta:
        pass

    def __str__(self):
        return self.name


class Ingredients(models.Model):
    name = models.CharField(
        'Название ингридиента',
        max_length=200,
    )
    # quantity = models.IntegerField() <- это должно быть не здесь!
    measurement_unit = models.CharField(
        'Единица измерения',
        max_length=200,
    )

    class Meta:
        pass

    def __str__(self):
        return self.name


class Recipe(models.Model):
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='recipes',
        verbose_name='Автор',
    )
    name = models.CharField(
        'Название рецепта',
        max_length=128,
    )
    image = models.ImageField(
        'Картинка',
        upload_to='recipes/images/',
        blank=True,
    )
    description = models.TextField(
        'Описание рецепта',
    )
    cooking_time = models.PositiveIntegerField()
    tags = models.ManyToManyField(Tag, through='TagRecipe')
    ingredients = models.ManyToManyField(
        Ingredients,
        through='IngredientsRecipe'
    )
    is_favorited = models.BooleanField(default=False)
    is_in_shopping_cart = models.BooleanField(default=False)

    class Meta:
        pass

    def __str__(self):
        return self.name


class TagRecipe(models.Model):
    tag = models.ForeignKey(Tag, on_delete=models.CASCADE)
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.tag} {self.recipe}'


class IngredientsRecipe(models.Model):
    ingredients = models.ForeignKey(Ingredients, on_delete=models.CASCADE)
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=6, decimal_places=2)

    def __str__(self):
        return f'{self.ingredients} {self.recipe}'
