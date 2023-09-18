from django.urls import path, include
from rest_framework import routers

from .views import *


router = routers.DefaultRouter()
router.register('houses', ObjectModelViewSet, basename='houses')
router.register('purchases', PurchaseModelViewSet, basename='purchases')

urlpatterns = [
    path('', include(router.urls)),
]
