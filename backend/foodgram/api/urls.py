# api/urls.py

from django.urls import include, path
from rest_framework.routers import DefaultRouter

from api.views import IngredientsViewSet, TagViewSet

router = DefaultRouter()
router.register('tags', TagViewSet, basename='tags')
router.register('ingredients', IngredientsViewSet, basename='ingredients')

urlpatterns = [
    path('', include(router.urls)),
]
