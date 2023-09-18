from django.shortcuts import render
from rest_framework import viewsets, mixins
from django.utils.decorators import method_decorator

from . import schemas
from . import models
from . import serializers


@method_decorator(name='list', decorator=schemas.main_page_schema.list())
class MainPageViewSet(mixins.ListModelMixin,
                      viewsets.GenericViewSet):
    queryset = models.MainPage.objects.all()
    serializer_class = serializers.MainPageModelSerializer


@method_decorator(name='list', decorator=schemas.back_photos_schema.list())
class BackPhotoViewSet(mixins.ListModelMixin,
                      viewsets.GenericViewSet):
    queryset = models.BackPhoto.objects.all()
    serializer_class = serializers.BackPhotoSerializer


@method_decorator(name='list', decorator=schemas.policy_agreement_schema.list())
class PolicyAgreementViewSet(mixins.ListModelMixin,
                      viewsets.GenericViewSet):
    queryset = models.PolicyAgreement.objects.all()
    serializer_class = serializers.PolicyAgreementsSerializer