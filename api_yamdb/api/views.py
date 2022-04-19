from django.shortcuts import get_object_or_404
import uuid
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, mixins, permissions, status, viewsets
from rest_framework.decorators import action
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.response import Response
from rest_framework.views import APIView
from review.models import Category, Genre, Title, User, Review
from rest_framework import mixins

from .serializers import (CategorySerializer, GenreSerializer,
                          ObtainTokenSerializer, SignUpSerializer,
                          TitleSerializer, UserSerializer, CommentSerializer,
                          UserSerializerReadOnly, TitleWriteSerializer,
                          ReviewSerializer)

from .filters import TitleFilter
from .permissions import (IsAdminOrReadOnly,
                          IsAdminModeratorAuthororReadOnly, IsAdmin)


class CategoryViewSet(mixins.CreateModelMixin,
                      mixins.ListModelMixin,
                      mixins.DestroyModelMixin,
                      viewsets.GenericViewSet):
    queryset = Category.objects.all()
    permission_classes = (IsAdminOrReadOnly,)
    filter_backends = (filters.SearchFilter,)
    search_fields = ('=name',)
    serializer_class = CategorySerializer
    lookup_field = ('slug')


class GenreViewSet(mixins.CreateModelMixin,
                   mixins.ListModelMixin,
                   mixins.DestroyModelMixin,
                   viewsets.GenericViewSet):
    queryset = Genre.objects.all()
    permission_classes = (IsAdminOrReadOnly,)
    serializer_class = GenreSerializer
    filter_backends = (filters.SearchFilter,)
    search_fields = ('=name',)
    lookup_field = ('slug')


class TitleViewSet(viewsets.ModelViewSet):
    queryset = Title.objects.all()
    permission_classes = (IsAdminOrReadOnly,)
    serializer_class = TitleSerializer
    filter_backends = (DjangoFilterBackend,)
    filterset_class = TitleFilter

    def get_serializer_class(self):
        if self.action in ['list', 'retrieve']:
            return TitleSerializer
        return TitleWriteSerializer


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (IsAdmin,)
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
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class APISignUp(APIView):
    def post(self, request):
        confirmation_code = str(uuid.uuid4())
        serializer = SignUpSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(
                username=request.data['username'],
                confirmation_code=confirmation_code
            )
            send_mail(
                'Код подтверждения на Yamdb',
                f'Для подтверждения регистрации используйте код:'
                f'{confirmation_code}',
                'admin@fake.ru',
                [serializer.data['email']],
                fail_silently=False
            )
            return Response(serializer.data['confirmation_code'],
                            status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors,
                            status=status.HTTP_400_BAD_REQUEST)


class APIObtainToken(APIView):
    def post(self, request):
        serializer = ObtainTokenSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            try:
                user = User.objects.get(
                    username=serializer.validated_data['username']
                )
            except User.DoesNotExist:
                return Response(status=status.HTTP_404_NOT_FOUND)
            if (
                serializer.validated_data['confirmation_code']
                == user.confirmation_code
            ):
                token = default_token_generator.make_token(request.user)
                return Response({'token': str(token)},
                                status=status.HTTP_201_CREATED
                                )
            return Response(serializer.errors,
                            status=status.HTTP_404_NOT_FOUND
                            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ReviewViewSet(viewsets.ModelViewSet):
    permission_classes = (IsAdminModeratorAuthororReadOnly,)
    serializer_class = ReviewSerializer

    def get_queryset(self):
        title = get_object_or_404(Title, pk=self.kwargs.get('id'))
        return title.reviews.all()

    def perfom_create(self, serializer):
        serializer.save(
            author=self.request.user,
            title=get_object_or_404(Title, pk=self.kwargs.get('id'))
        )


class CommentViewSet(viewsets.ModelViewSet):
    permission_classes = (IsAdminModeratorAuthororReadOnly,)
    serializer_class = CommentSerializer
    pagination_class = LimitOffsetPagination

    def get_queryset(self):
        review = get_object_or_404(
            Review,
            id=self.kwargs.get('review_id')
        )
        queryset = review.comments.all()
        return queryset

    def perform_create(self, serializer):
        review = get_object_or_404(
            Review,
            id=self.kwargs.get('review_id')
        )
        serializer.save(
            author=self.request.user,
            review=review
        )
