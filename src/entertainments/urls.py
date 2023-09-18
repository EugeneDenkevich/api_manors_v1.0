from django.urls import path, include
from rest_framework import routers

from .views import *


router = routers.DefaultRouter()
router.register('entertainments', EntertainmentViewSet, basename='entertainment')
router.register('galeries', GaleryViewSet, basename='galeries')
router.register('nearests', NearestPlaceViewSet, basename='nearests')


urlpatterns = [
    path('', include(router.urls)),
]
