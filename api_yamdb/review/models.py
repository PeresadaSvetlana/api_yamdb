from django.db import models
from users.models import User


class Categories(models.Model):
    name = models.CharField(
        max_length=256,
        verbose_name='Наименование категории'
    )
    slug = models.SlugField(
        max_length=50,
        unique=True,
        verbose_name='Название')

    def __str__(self):
        return self.name


class Genres(models.Model):
    name = models.CharField(
        max_length=256,
        verbose_name='Наименование жанра'
    )
    slug = models.SlugField(
        unique=True,
        max_length=50,
        verbose_name='Название'
    )

    def __str__(self):
        return self.name


class Titles(models.Model):
    name = models.CharField(
        max_length=256,
        verbose_name='Наименование'
    )
    year = models.IntegerField()
    description = models.TextField(
        blank=True,
        null=True,
        verbose_name='Описание')
    genre = models.ManyToManyField(
        Genres,
    )
    category = models.ForeignKey(
        Categories,
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        related_name='review',
        verbose_name='Категория'
    )

    def __str__(self):
        return self.name


class Comments(models.Model):
    text = models.TextField()
    author = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='comments')
    pub_date = models.DateTimeField('Дата публикации', auto_now_add=True)


class Review(models.Model):
    text = models.TextField()
    author = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='review')
    score = models.TextField()
    pub_date = models.DateTimeField('Дата публикации', auto_now_add=True)
