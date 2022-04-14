from .models import Categories, Genres, Titles
from rest_framework import serializers


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


class ObtainTokenSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('username', 'confirmation_code')