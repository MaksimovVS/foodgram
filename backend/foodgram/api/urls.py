# api/urls.py

from django.urls import include, path
from rest_framework.routers import DefaultRouter

from api.views import TagViewSet

router = DefaultRouter()
router.register('tags', TagViewSet, basename='tags')

urlpatterns = [
    path('', include(router.urls)),
]
