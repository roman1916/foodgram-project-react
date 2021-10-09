from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import (
    IngredientsViewSet,
    TagsViewSet,
    RecipeViewSet
)

router = DefaultRouter()

router.register('ingredients', IngredientsViewSet,
                basename='ingredients')
router.register('tags', TagsViewSet, basename='tags')
router.register('recipes', RecipeViewSet, basename='recipes')

urlpatterns = [
    path('', include(router.urls)),
]
