from django.db import models
from users.models import User
import datetime as dt
from django.core.exceptions import ValidationError


class Category(models.Model):
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

    class Meta:
        ordering = ['-id']


class Genre(models.Model):
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

    class Meta:
        ordering = ['-id']


class Title(models.Model):
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
        Genre, related_name='genre', through='GenreTitle'
    )
    category = models.ForeignKey(
        Category,
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        related_name='title',
        verbose_name='Категория'
    )

    def __str__(self):
        return self.name

    def validate(year):
        if dt.datetime.now().year <= year:
            raise ValidationError(
                'Этот год еще не наступил!'
            )
        return year

    class Meta:
        ordering = ['-id']


class GenreTitle(models.Model):
    title = models.ForeignKey(Title, on_delete=models.CASCADE)
    genre = models.ForeignKey(Genre, on_delete=models.CASCADE)


class Review(models.Model):
    title = models.ForeignKey(
        Title,
        on_delete=models.CASCADE,
        related_name='review',
        blank=True,
        null=True
    )
    text = models.TextField()
    author = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='review')
    score = models.IntegerField(
        'Оценка',
        default=0
    )
    pub_date = models.DateTimeField(
        'Дата публикации',
        auto_now_add=True
    )

    class Meta:
        ordering = ['-pub_date']
        constraints = [
            models.UniqueConstraint(
                fields=['author', 'title'], name="unique_review")
        ]


class Comment(models.Model):
    review = models.ForeignKey(
        Review, on_delete=models.CASCADE,
        related_name='comments',
        blank=True,
        null=True
    )
    text = models.TextField()
    author = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='comments')
    pub_date = models.DateTimeField(
        'Дата публикации',
        auto_now_add=True
    )

    def __str__(self):
        return self.author
