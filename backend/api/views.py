from django.db.models import Sum
from django.http.response import HttpResponse
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from djoser.views import UserViewSet
from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.permissions import (IsAuthenticated,
                                        IsAuthenticatedOrReadOnly)
from rest_framework.response import Response

from api.filters import IngredientFilter, RecipesFilter
from api.permissions import IsAuthorOrReadOnly
from api.serializers import (CreateRecipeSerializer, FollowSerializer,
                             IngredientSerializer, RecipeSerializer,
                             TagSerializer, UsersSerializer)
from app.models import Favorite, Follow, ShoppingCart
from ingredient.models import Ingredient
from recipe.models import IngredientRecipe, Recipe, Tag
from users.models import User

from .pagination import PageFieldPagination


class UsersViewSet(UserViewSet):
    """Вьюсет для пользователей и подписок. """

    queryset = User.objects.all()
    serializer_class = UsersSerializer
    pagination_class = PageFieldPagination

    @action(
            detail=True,
            methods=['POST', 'DELETE'],
            permission_classes=(IsAuthenticated,)
            )
    def subscribe(self, request, id):
        user = request.user
        author = get_object_or_404(User, pk=id)
        if request.method == 'POST':
            serializer = FollowSerializer(
                                          author,
                                          data=request.data,
                                          context={'request': request}
                                          )
            serializer.is_valid(raise_exception=True)
            Follow.objects.create(user=user, author=author)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        if request.method == 'DELETE':
            get_object_or_404(Follow, user=user, author=author).delete()
            return Response({'detail': 'Вы отписались'},
                            status=status.HTTP_204_NO_CONTENT)

    @action(
            detail=False,
            permission_classes=(IsAuthenticated,)
    )
    def subscriptions(self, request):
        serializer = FollowSerializer(
            self.paginate_queryset(
                User.objects.filter(following__user=request.user)
            ),
            many=True,
            context={'request': request}
        )
        return self.get_paginated_response(serializer.data)


class RecipeViewSet(viewsets.ModelViewSet):
    """Вьюсет для рецептов."""

    queryset = Recipe.objects.all()
    serializer_class = RecipeSerializer
    permission_classes = (IsAuthorOrReadOnly,)
    filter_backends = (DjangoFilterBackend, )
    filterset_class = RecipesFilter
    pagination_class = PageFieldPagination

    def get_queryset(self):
        queryset = Recipe.objects.all()
        return queryset

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return RecipeSerializer
        return CreateRecipeSerializer

    def recipe_add(self, model, request, pk):
        user = request.user
        recipe = get_object_or_404(Recipe, pk=pk)
        serializer = RecipeSerializer(recipe)
        if not model.objects.filter(recipe=recipe, user=user).exists():
            model.objects.create(recipe=recipe, user=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response({'errors': 'Рецепт уже был добавлен.'},
                        status=status.HTTP_400_BAD_REQUEST)

    def recipe_delete(self, model, request, pk):
        get_object_or_404(
                        model,
                        user=request.user,
                        recipe=get_object_or_404(Recipe, pk=pk)).delete()
        return Response({'detail': 'Рецепт удален.'},
                        status=status.HTTP_204_NO_CONTENT)

    @action(
            detail=True,
            methods=['POST', 'DELETE'],
            permission_classes=(IsAuthenticated,)
    )
    def favorite(self, request, pk):
        if request.method == 'POST':
            return self.recipe_add(Favorite, request, pk)
        return self.recipe_delete(Favorite, request, pk)

    @action(
            detail=True,
            methods=['POST', 'DELETE'],
            permission_classes=(IsAuthenticated,)
    )
    def shopping_cart(self, request, pk=None):
        get_object_or_404(
            ShoppingCart,
            user=request.user.id,
            recipe=get_object_or_404(Recipe, id=pk)
        ).delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    @action(
        detail=False,
        methods=['GET'],
        permission_classes=(IsAuthenticated,)
    )
    def download_shopping_cart(self, request):
        ingredients = IngredientRecipe.objects.filter(
            recipe__shopping_cart__user=request.user).values(
            'ingredient__name',
            'ingredient__measurement_unit').annotate(
            amount=Sum('amount')
        )
        data = []
        for ingredient in ingredients:
            data.append(
                f'{ingredient["ingredient__name"]} - '
                f'{ingredient["amount"]} '
                f'{ingredient["ingredient__measurement_unit"]}'
            )
        content = 'Список покупок:\n\n' + '\n'.join(data)
        filename = 'shopping_cart.txt'
        request = HttpResponse(content, content_type='text/plain')
        request['Content-Disposition'] = f'attachment; filename={filename}'
        return request


class TagViewSet(viewsets.ModelViewSet):
    """Вьюсет для тегов."""

    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    permission_classes = (IsAuthenticatedOrReadOnly, )
    pagination_class = None


class IngredientViewSet(viewsets.ModelViewSet):
    """Вьюсет для ингредиентов."""

    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializer
    permission_classes = (IsAuthenticatedOrReadOnly, )
    pagination_class = None
    filter_backends = (IngredientFilter, )
    search_fields = ('^name', )
