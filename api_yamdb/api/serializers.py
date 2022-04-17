from django.core.exceptions import ValidationError
from rest_framework import serializers
from review.models import Categories, Genres, Titles
from users.models import User
import datetime as dt


class CategoriesSerializer(serializers.ModelSerializer):

    class Meta:
        fields = ('name', 'slug')
        model = Categories


class GenresSerializer(serializers.ModelSerializer):

    class Meta:
        fields = ('name', 'slug')
        model = Genres


class TitlesSerializer(serializers.ModelSerializer):

    class Meta:
        fields = '__all__'
        model = Titles

    def validate(self, data):
        if dt.datetime.now().year <= self.year:
            raise serializers.ValidationError(
                "Этот год еще не наступил!"
            )
        return data


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        fields = '__all__'
        model = User


class SignUpSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ('email', 'username')

    def validate(self, value):
        if value == 'me':
            raise ValidationError(message='Запрещенное имя пользователя!')


class ObtainTokenSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ('username', 'confirmation_code')
