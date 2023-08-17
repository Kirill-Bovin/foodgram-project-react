from django_filters.rest_framework import FilterSet, filters
from rest_framework.filters import SearchFilter

from ingredient.models import Ingredient
from recipe.models import Recipe, Tag


class IngredientFilter(SearchFilter):
    """Фильт ингредиентов."""

    name = filters.CharFilter(lookup_expr='istartswith')

    class Meta:
        model = Ingredient
        fields = ('name',)


class RecipesFilter(FilterSet):
    """Фильт рецептов."""

    tags = filters.ModelMultipleChoiceFilter(
        field_name='tags__slug',
        queryset=Tag.objects.all(),
        to_field_name='slug',
    )
    is_favorited = filters.NumberFilter(method='receive_is_favorited')
    is_in_shopping_cart = filters.NumberFilter(
        method='receive_is_in_shopping_cart'
    )

    class Meta:
        model = Recipe
        fields = ('tags', 'author', 'is_favorited', 'is_in_shopping_cart')

    def receive_is_favorited(self, queryset, name, value):
        if value and self.request.user.is_authenticated:
            return queryset.filter(favorites__user=self.request.user)
        return queryset

    def receive_is_in_shopping_cart(self, queryset, name, value):
        if value and self.request.user.is_authenticated:
            return queryset.filter(shopping_list__user=self.request.user)
        return queryset
