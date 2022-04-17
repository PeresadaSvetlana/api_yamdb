from rest_framework import viewsets, filters, status, permissions
from rest_framework.views import APIView
from django.core.mail import send_mail
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.permissions import IsAuthenticatedOrReadOnly

from rest_framework.response import Response
from rest_framework import status, permissions
from .permissions import IsAdminOrReadOnly, IsAdminOnly
from review.models import Categories, Genres, Titles, User
from rest_framework import mixins
from .serializers import (CategoriesSerializer, GenresSerializer,
                          TitlesSerializer, SignUpSerializer,
                          ObtainTokenSerializer, UserSerializer
                          )


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
        IsAdminOnly,
    )
    lookup_field = 'username'


class APISignUp(APIView):
    def post(self, request):
        serializer = SignUpSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            send_mail(
                'Тема письма',
                'Текст письма.',
                'from@example.com',
                ['to@example.com'],
                fail_silently=False,
            )
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class APIObtainToken(APIView):
    def post(self, request):
        serializer = ObtainTokenSerializer(data=request.data)
