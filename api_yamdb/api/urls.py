from django.urls import include, path
from rest_framework import routers

from .views import (APIObtainToken, APISignUp, CategoriesViewSet,
                    GenresViewSet, TitlesViewSet, UserViewSet, ReviewViewSet,
                    CommentsViewSet)

router = routers.DefaultRouter()
router.register(r'categories', CategoriesViewSet)
router.register(r'genres', GenresViewSet)
router.register(r'titles', TitlesViewSet)
router.register(r'users', UserViewSet)
router.register(
    r'titles/(?P<title_id>\d+)/reviews',
    ReviewViewSet,
    basename='reviews'
)
router.register(
    r'titles/(?P<title_id>[0-9]+)/reviews/(?P<review_id>[0-9]+)/comments',
    CommentsViewSet,
    basename='comments'
)

urlpatterns = [

    path('v1/', include(router.urls)),
    path('v1/auth/token/', APIObtainToken.as_view()),
    path('v1/auth/signup/', APISignUp.as_view()),
]
