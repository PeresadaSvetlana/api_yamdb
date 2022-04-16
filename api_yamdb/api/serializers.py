<<<<<<< HEAD
from django.core.exceptions import ValidationError
from rest_framework import serializers
from review.models import Categories, Genres, Titles
from users.models import User
=======
from review.models import Categories, Genres, Titles
from users.models import User
from rest_framework import serializers
>>>>>>> ae03824cc631b121a7ec5770cd5b7ee7e1d092e9


class CategoriesSerializer(serializers.ModelSerializer):

    class Meta:
        fields = '__all__'
        model = Categories


class GenresSerializer(serializers.ModelSerializer):

    class Meta:
        fields = '__all__'
        model = Genres


class TitlesSerializer(serializers.ModelSerializer):

    class Meta:
        fields = '__all__'
        model = Titles


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
