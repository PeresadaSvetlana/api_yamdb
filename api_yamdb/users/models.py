from django.contrib.auth.models import AbstractUser
from django.db import models

USER = 'User'
ROLE_CHOICES = [
    ('USER', 'User'),
    ('ADMIN', 'Admin'),
    ('MODERATOR', 'Moderator')
]



class User(AbstractUser):
<<<<<<< HEAD
    username = models.ForeignKey(blank=False)
    email = models.EmailField(blank=False)
    role = models.CharField(choices=ROLE_CHOICES, default=USER)
    bio = models.TextField('Биография', blank=True)
=======
    
    email = models.EmailField(blank=False)
    role = models.CharField(max_length=100, choices=ROLE_CHOICES,
        default=USER)
    bio = models.TextField('Биография', blank=True) 
>>>>>>> f15634f0faef602ef8b1d5e605d57299a2adbd1d
    first_name = models.CharField(max_length=20, blank=True)
    last_name = models.CharField(max_length=20, blank=True)
