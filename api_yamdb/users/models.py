from datetime import datetime, timedelta

import jwt
from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.db import models

USER = 'User'
ADMIN = 'Admin'
MODERATOR = 'Moderator'
ROLE_CHOICES = [
    ('USER', 'User'),
    ('ADMIN', 'Admin'),
    ('MODERATOR', 'Moderator')
]


class User(AbstractUser):
<<<<<<< HEAD
    username = models.CharField(max_length=100, unique=True)
    email = models.EmailField(blank=False, unique=True)
    role = models.CharField(max_length=10, choices=ROLE_CHOICES,
                            default=USER)
    bio = models.TextField(max_length=1000, blank=True)
=======
    username = models.CharField(max_length=200, unique=True)
    email = models.EmailField(blank=False)
    role = models.CharField(max_length=100, choices=ROLE_CHOICES,
        default=USER)
    bio = models.TextField('Биография', blank=True) 
>>>>>>> ae03824cc631b121a7ec5770cd5b7ee7e1d092e9
    first_name = models.CharField(max_length=20, blank=True)
    last_name = models.CharField(max_length=20, blank=True)
    confirmation_code = models.CharField(max_length=14, default='1234')

    USERNAME_FIELD = 'email'

    REQUIRED_FIELDS = ('username',)

    def __str__(self):

        return self.username

    @property
    def token(self):
        return self._generate_jwt_token()

    def _generate_jwt_token(self):
        dt = datetime.now() + timedelta(days=60)

        token = jwt.encode({
            'id': self.pk,
            'exp': int(dt.strftime('%s'))
        }, settings.SECRET_KEY, algorithm='HS256')

        return token.decode('utf-8')

    @property
    def is_admin(self):
        return self.role == ADMIN

    @property
    def is_moderator(self):
        return self.role == MODERATOR

    @property
    def is_user(self):
        return self.role == USER
