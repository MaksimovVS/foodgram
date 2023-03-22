# recipes/models.py

from django.contrib.auth import get_user_model
from django.db import models

User = get_user_model()


class Tag(models):
    name = models.CharField(
        'Название тега',
        max_length=128,
    )
    color = models.CharField(max_length=7)
    slug = models.CharField(
        'slug Тега',
        max_length=32,
    )

    class Meta:
        pass

    def __str__(self):
        return self.name


class Ingredients(models):
    name = models.CharField(
        'Название ингридиента',
        max_length=128,
    )
    quantity = models.IntegerField()
    unit = models.CharField(
        'Единица измерения',
        max_length=10,
    )

    class Meta:
        pass

    def __str__(self):
        return self.name


class Recipe(models):
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
    cooking_time = models.IntegerField()
    tags = models.ManyToManyField(Tag, through='TagRecipe')
    ingredients = models.ManyToManyField(
        Ingredients,
        through='IngredientsRecipe'
    )

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

    def __str__(self):
        return f'{self.ingredients} {self.recipe}'
