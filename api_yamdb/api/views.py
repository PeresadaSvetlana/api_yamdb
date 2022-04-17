from rest_framework import viewsets, filters, status, permissions
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.permissions import IsAuthenticatedOrReadOnly
import uuid
from django.shortcuts import get_object_or_404
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail
from rest_framework import filters, permissions, status, viewsets, mixins
from rest_framework.decorators import action
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.response import Response
from rest_framework.views import APIView
from review.models import Categories, Genres, Titles, User, Comments
from rest_framework import mixins

from .permissions import (IsAdminOrReadOnly, IsAdminOrSuperOnly,
                          StaffOrAuthorOrReadOnly)
from .serializers import (CategoriesSerializer, GenresSerializer,
                          ObtainTokenSerializer, SignUpSerializer,
                          TitlesSerializer, UserSerializer, CommentsSerializer,
                          UserSerializerReadOnly)


class CategoriesViewSet(mixins.CreateModelMixin,
                        mixins.ListModelMixin,
                        mixins.DestroyModelMixin,
                        viewsets.GenericViewSet):
    queryset = Categories.objects.all()
    permission_classes = (IsAdminOrReadOnly, IsAuthenticatedOrReadOnly,)
    filter_backends = (filters.SearchFilter,)
    search_fields = ('=name',)
    serializer_class = CategoriesSerializer
    lookup_field = ('slug')


class GenresViewSet(mixins.CreateModelMixin,
                    mixins.ListModelMixin,
                    mixins.DestroyModelMixin,
                    viewsets.GenericViewSet):
    queryset = Genres.objects.all()
    permission_classes = (IsAdminOrReadOnly,)
    serializer_class = GenresSerializer
    filter_backends = (filters.SearchFilter,)
    search_fields = ('=name',)


class TitlesViewSet(viewsets.ModelViewSet):
    queryset = Titles.objects.all()
    permission_classes = (IsAdminOrReadOnly,)
    serializer_class = TitlesSerializer
    filter_backends = (DjangoFilterBackend,)
    filterset_fields = ('genre__slug', 'category__slug', 'name', 'year')


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (
        permissions.IsAuthenticated,
        IsAdminOrSuperOnly,
    )
    pagination_class = LimitOffsetPagination
    filter_backends = (filters.SearchFilter,)
    search_fields = ('username',)
    lookup_field = 'username'

    @action(methods=['GET', 'PATCH'],
            detail=False,
            permission_classes=[permissions.IsAuthenticated],
            url_path='me')
    def change_info(self, request):
        if request.method == 'PATCH':
            serializer = UserSerializerReadOnly(
                request.user,
                data=request.data,
                partial=True
            )
            serializer.is_valid()
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)


class APISignUp(APIView):

    def post(self, request):
        confirmation_code = str(uuid.uuid4())
        serializer = SignUpSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            send_mail(
                'Ваш код',
                'Для получения токена',
                f'{confirmation_code}',
                [serializer.data['email']],
                fail_silently=False,
            )
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class APIObtainToken(APIView):

    def post(self, request):
        serializer = ObtainTokenSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = serializer.validated_data
        user = User.objects.get(username=data['username'])
        if data.get('confirmation_code') == user.confirmation_code:
            token = default_token_generator.make_token(request.user)
            return Response({'token': str(token)},
                            status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
