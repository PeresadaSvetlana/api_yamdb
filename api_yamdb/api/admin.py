from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from reviews.models import Category, Genre, Review, Title, Comment


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = list_display = ('name', 'slug')
    empty_value_display = '-пусто-'


@admin.register(Genre)
class GenreAdmin(admin.ModelAdmin):
    list_display = list_display = ('name', 'slug')
    empty_value_display = '-пусто-'


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = list_display = (
        'title', 'text', 'author', 'score', 'pub_date'
    )
    empty_value_display = '-пусто-'


@admin.register(Title)
class TitleAdmin(admin.ModelAdmin):
    list_display = list_display = (
        'name', 'year', 'description', 'category'
    )
    empty_value_display = '-пусто-'


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = list_display = (
        'review', 'text', 'author', 'pub_date'
    )
    empty_value_display = '-пусто-'
