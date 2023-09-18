from django.urls import path, include
from rest_framework import routers

from .views import *


router = routers.DefaultRouter()
router.register('info', InfoModelViewSet, basename='info')
router.register('dish', DishModelViewSet, basename='dish')
router.register('meal', MealModelViewSet, basename='meal')
router.register('rule', RuleModelViewSet, basename='rule')


urlpatterns = [
    path('', include(router.urls)),
]
