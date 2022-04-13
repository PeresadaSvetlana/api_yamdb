from django.urls import include, path
from rest_framework import routers

from .views import CategoriesViewSet, GenresViewSet, TitlesViewSet

router = routers.DefaultRouter()
router.register(r'categories', CategoriesViewSet)
router.register(r'groups', GenresViewSet)
router.register(r'follow', TitlesViewSet)


urlpatterns = [
    path('v1/', include(router.urls))
]
