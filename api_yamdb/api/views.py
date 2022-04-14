from rest_framework import viewsets
from rest_framework.views import APIView
from rest_framework.pagination import LimitOffsetPagination
from django.core.mail import send_mail

from rest_framework.response import Response
from rest_framework import status
from .permissions import IsAdminOrReadOnly, IsAuthenticated, IsAdminOnly
from .models import Categories, Genres, Titles, User
from .serializers import (CategoriesSerializer, GenresSerializer,
                          TitlesSerializer, SignUpSerializer,
                          ObtainTokenSerializer, UserSerializer
                          )


class CategoriesViewSet(viewsets.ModelViewSet):
    queryset = Categories.objects.all()
    pagination_class = LimitOffsetPagination
    permission_classes = (IsAdminOrReadOnly,)
    serializer_class = CategoriesSerializer


class GenresViewSet(viewsets.ModelViewSet):
    queryset = Genres.objects.all()
    pagination_class = LimitOffsetPagination
    permission_classes = (IsAdminOrReadOnly,)
    serializer_class = GenresSerializer


class TitlesViewSet(viewsets.ModelViewSet):
    queryset = Titles.objects.all()
    pagination_class = LimitOffsetPagination
    permission_classes = (IsAdminOrReadOnly,)
    serializer_class = TitlesSerializer


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (
        IsAuthenticated,
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
