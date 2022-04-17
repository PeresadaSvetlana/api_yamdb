from django.contrib.auth.models import AbstractUser
from django.db import models

USER = 'User'
ROLE_CHOICES = [
    ('USER', 'User'),
    ('ADMIN', 'Admin'),
    ('MODERATOR', 'Moderator')
]


class User(AbstractUser):
    username = models.CharField(max_length=200, unique=True)
    email = models.EmailField(blank=False)
    role = models.CharField(
        max_length=100,
        choices=ROLE_CHOICES,
        default=USER
    )
    bio = models.TextField('Биография', blank=True)
    first_name = models.CharField(max_length=20, blank=True)
    last_name = models.CharField(max_length=20, blank=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)

    @property
    def is_admin(self):
        return self.role == 'Admin' or self.is_superuser

    @property
    def is_moderator(self):
        return self.role == 'Moderator'

    @property
    def is_user(self):
        return self.role == 'User'
