from django.contrib import admin

from app.models import Favorite

from .models import IngredientRecipe, Recipe, Tag


@admin.register(Recipe)
class RecipeAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'author', 'in_favorites', )
    list_filter = ('name', 'author', 'tags', )
    search_fields = ('name', )
    empty_value_display = '-пусто-'

    def in_favorites(self, obj):
        return Favorite.objects.filter(recipe=obj).count()

    in_favorites.short_description = 'Добавлен в избранное'


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'color', 'slug')
    list_filter = ('name', 'color',)
    empty_value_display = '-пусто-'


@admin.register(IngredientRecipe)
class IngredientRecipeAdmin(admin.ModelAdmin):
    list_display = ('id', 'recipe', 'ingredient', 'amount')
    list_editable = ('recipe', 'ingredient', 'amount')