import uuid

from django.contrib.auth.models import AbstractUser
from django.db import models

USER = 'user'
ADMIN = 'admin'
MODERATOR = 'moderator'
ROLE_CHOICES = [
    (USER, USER),
    (ADMIN, ADMIN),
    (MODERATOR, MODERATOR)
]


class User(AbstractUser):
    username = models.CharField(
        max_length=100,
        unique=True,
        verbose_name='Ник'
    )
    email = models.EmailField(
        blank=False,
        unique=True,
        verbose_name='Почта'
    )
    role = models.CharField(
        max_length=10,
        choices=ROLE_CHOICES,
        default=USER,
        verbose_name='Роль'
    )
    bio = models.TextField(
        max_length=1000,
        blank=True,
        verbose_name='Биография'
    )
    first_name = models.CharField(
        max_length=20,
        blank=True,
        verbose_name='Имя'
    )
    last_name = models.CharField(
        max_length=20,
        blank=True,
        verbose_name='Фамилия'
    )
    confirmation_code = models.CharField(
        max_length=14,
        default=uuid.uuid4(),
        verbose_name='Код'
    )

    class Meta:
        ordering = ['id']
        verbose_name = 'user'
        verbose_name_plural = 'users'

    def __str__(self):

        return self.username

    def is_admin(self):
        return self.role == self.ADMIN

    def is_moderator(self):
        return self.role == self.MODERATOR
