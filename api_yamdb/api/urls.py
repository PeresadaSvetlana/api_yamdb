from django.urls import include, path
from rest_framework import routers

from .views import (APIObtainToken, APISignUp, CategoryViewSet,
                    GenreViewSet, TitleViewSet, UserViewSet, ReviewViewSet,
                    CommentViewSet)

router = routers.DefaultRouter()
router.register(r'categories', CategoryViewSet)
router.register(r'genres', GenreViewSet)
router.register(r'titles', TitleViewSet)
router.register(r'users', UserViewSet)
router.register(
    r'titles/(?P<title_id>\d+)/reviews',
    ReviewViewSet,
    basename='review'
)
router.register(
    r'titles/(?P<title_id>[0-9]+)/reviews/(?P<review_id>[0-9]+)/comments',
    CommentViewSet,
    basename='comments'
)

urlpatterns = [

    path('v1/', include(router.urls)),
    path('v1/auth/token/', APIObtainToken.as_view()),
    path('v1/auth/signup/', APISignUp.as_view()),
]
