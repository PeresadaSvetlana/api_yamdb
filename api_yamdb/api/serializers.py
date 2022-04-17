from django.core.exceptions import ValidationError
from rest_framework import serializers
from review.models import Categories, Genres, Titles, Comments
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


class CommentsSerializer(serializers.ModelSerializer):

    class Meta:
        fields = ('review', 'author')
        model = Comments


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        fields = '__all__'
        model = User


class SignUpSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ('email', 'username')

    def validate(self, data):
        if data['username'] == 'me':
            raise ValidationError(message='Запрещенное имя пользователя!')
        return data


class ObtainTokenSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ('username', 'confirmation_code')


class UserSerializerReadOnly(serializers.ModelSerializer):
    role = serializers.CharField(read_only=True)

    class Meta:
        fields = (
            'first_name',
            'last_name',
            'username',
            'bio',
            'email',
            'role'
        )
        model = User
