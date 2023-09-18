from django.urls import path, include
from rest_framework import routers

from . import views


router = routers.DefaultRouter()
router.register('main-page', views.MainPageViewSet, basename='main-page')
router.register('back-photos', views.BackPhotoViewSet, basename='page-name')
router.register('policy-agreement', views.PolicyAgreementViewSet, basename='policy-agreement')


urlpatterns = [
    path('', include(router.urls)),
]