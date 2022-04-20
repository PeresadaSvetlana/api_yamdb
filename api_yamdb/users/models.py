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
    username = models.CharField(max_length=100, unique=True)
    email = models.EmailField(blank=False, unique=True)
    role = models.CharField(max_length=10, choices=ROLE_CHOICES,
                            default=USER)
    bio = models.TextField(max_length=1000, blank=True)
    first_name = models.CharField(max_length=20, blank=True)
    last_name = models.CharField(max_length=20, blank=True)
    confirmation_code = models.CharField(max_length=14, default='1234')

    def __str__(self):

        return self.username

    @property
    def is_admin(self):
        return self.role == ADMIN

    @property
    def is_moderator(self):
        return self.role == MODERATOR

    @property
    def is_user(self):
        return self.role == USER
