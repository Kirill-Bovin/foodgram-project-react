from django.core.validators import (MaxValueValidator, MinValueValidator,
                                    RegexValidator)
from django.db import models
from django.db.models.constraints import UniqueConstraint

from ingredient.models import Ingredient
from users.models import User


class Tag(models.Model):
    """Модель тегов."""

    name = models.CharField(
        max_length=254,
        unique=True,
        verbose_name='Название тега',
    )
    color = models.CharField(
        max_length=7,
        unique=True,
        verbose_name='Цвет',
        validators=[
            RegexValidator(
                r'^#([A-Fa-f0-9]){3,6}$',
                message='Введите цвет в формате HEX'
            ),
        ],
    )
    slug = models.SlugField(
        unique=True,
        verbose_name='Уникальный слаг',
    )

    class Meta:
        ordering = ['name']
        verbose_name = 'Тег'
        verbose_name_plural = 'Теги'

    def __str__(self):
        return self.name


class Recipe(models.Model):
    """Модель рецептов."""

    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name='Автор публикации',
        related_name='recipe',
    )
    name = models.CharField(
        max_length=255,
        verbose_name='Название рецепта',
    )
    ingredients = models.ManyToManyField(
        Ingredient,
        through='IngredientRecipe',
        verbose_name='Ингредиенты',
    )
    image = models.ImageField(
        upload_to='media/',
        blank=True,
        verbose_name='Фото рецепта'
    )
    text = models.TextField(
        max_length=2000,
        verbose_name='Текст рецепта',
    )
    tags = models.ManyToManyField(
        Tag,
        verbose_name='Тег',
    )
    cooking_time = models.PositiveSmallIntegerField(
        validators=[
            MinValueValidator(
                1, message='Минимальное время готовки не менее 1 минуты!'),
            MaxValueValidator(
                720, message='Максимальное время готовки не более 720 минут!')
        ],
        verbose_name='Время приготовления в минутах',
    )
    pub_date = models.DateTimeField(
        verbose_name='Дата публикации',
        auto_now_add=True,
    )

    class Meta:
        ordering = ['-pub_date']
        verbose_name = 'Рецепт'
        verbose_name_plural = 'Рецепты'

    def __str__(self):
        return f'{self.author}, {self.name}'


class IngredientRecipe(models.Model):
    """Модель для количества ингредиентов в рецепте."""

    ingredient = models.ForeignKey(
        Ingredient,
        on_delete=models.CASCADE,
        related_name='ingredient',
    )
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        related_name='recipe',
    )
    amount = models.PositiveIntegerField(
        verbose_name='Количество ингридиентов',
        validators=[
            MinValueValidator(
                1, message='Ингридиентов должно быть не менее 1!'),
            MaxValueValidator(
                2000, message='ингридиентов должно быть не более 2000!')
        ]
    )

    class Meta:
        verbose_name = 'Количество ингредиента в рецепте'
        verbose_name_plural = 'Количество ингредиентов в рецепте'
        constraints = [
            UniqueConstraint(
                fields=['ingredient', 'recipe'],
                name='unique_ingredient',
            ),
        ]
