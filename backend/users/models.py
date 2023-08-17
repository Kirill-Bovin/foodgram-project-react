from django.contrib.auth.models import AbstractUser
from django.db import models
from django.db.models.constraints import UniqueConstraint

from .validators import validate_username


class User(AbstractUser):
    username = models.CharField(
        'Имя пользователя',
        max_length=150,
        unique=True,
        validators=(validate_username, ),
    )
    email = models.EmailField(
        verbose_name='Электронная почта',
        max_length=254,
        unique=True,
    )
    first_name = models.TextField(
        max_length=150,
        blank=True
    )
    last_name = models.TextField(
        max_length=150,
        blank=True
    )

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'
        constraints = [
            UniqueConstraint(fields=('username', 'email'),
                             name='unique_user')
        ]

    def __str__(self):
        return self.username
