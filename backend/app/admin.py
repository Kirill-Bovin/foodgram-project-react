from django.contrib import admin

from app.models import Favorite, Follow, ShoppingCart


@admin.register(Favorite)
class FavoriteAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'recipe', )
    search_fields = ('user', 'recipe', )
    empty_value_display = '-пусто-'


@admin.register(ShoppingCart)
class ShoppingCartAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'recipe', )
    search_fields = ('user', 'recipe', )
    empty_value_display = '-пусто-'


@admin.register(Follow)
class FollowAdmin(admin.ModelAdmin):
    list_display = (
        'id', 'user', 'author',)
    list_editable = ('user', 'author')
    empty_value_display = '-пусто-'
