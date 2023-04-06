# recipes/admin.py

from django.contrib import admin
from recipes.models import Favorite, Ingredient, IngredientRecipe, Recipe, Tag


class TagAdmin(admin.ModelAdmin):
    list_display = ("pk", "name", "color", "slug")
    list_editable = ("color",)
    search_fields = ("name", "color", "slug")


class IngredientAdmin(admin.ModelAdmin):
    list_display = (
        "pk",
        "name",
        "measurement_unit",
    )
    search_fields = ("measurement_unit",)
    list_filter = ("measurement_unit",)


class IngredientRecipeAdmin(admin.ModelAdmin):
    list_display = ("pk", "ingredient", "recipe", "amount")
    search_fields = ("recipe__name",)


class IngredientRecipeInline(admin.TabularInline):
    model = IngredientRecipe


class RecipeAdmin(admin.ModelAdmin):
    list_display = ("pk", "name", "author")
    search_fields = ("name", "author__username", "author__email")
    inlines = (IngredientRecipeInline,)


class FavoriteAdmin(admin.ModelAdmin):
    list_display = ("pk", "user", "recipe")
    search_fields = ("user__username", "user__email", "recipe__name")


admin.site.register(Favorite, FavoriteAdmin)
admin.site.register(Ingredient, IngredientAdmin)
admin.site.register(IngredientRecipe, IngredientRecipeAdmin)
admin.site.register(Recipe, RecipeAdmin)
admin.site.register(Tag, TagAdmin)
