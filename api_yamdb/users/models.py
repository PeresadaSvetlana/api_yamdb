from django.contrib.auth.models import AbstractUser
from django.db import models

USER = 'User'
ROLE_CHOICES = [
        ('USER', 'User'),
        ('ADMIN', 'Admin'),
        ('MODERATOR', 'Moderator')
    ]


class User(AbstractUser):
    
    email = models.EmailField(blank=False)
    role = models.CharField(max_length=100, choices=ROLE_CHOICES,
        default=USER)
    bio = models.TextField('Биография', blank=True) 
    first_name = models.CharField(max_length=20, blank=True)
    last_name = models.CharField(max_length=20, blank=True)
