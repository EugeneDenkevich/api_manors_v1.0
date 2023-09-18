from rest_framework.viewsets import GenericViewSet, mixins
from django.utils.decorators import method_decorator

from .schemas import *
from .models import *
from .serializers import *


@method_decorator(name='retrieve', decorator=entertainment_schema.retrieve())
@method_decorator(name='list', decorator=entertainment_schema.list())
class EntertainmentViewSet(mixins.ListModelMixin,
                           mixins.RetrieveModelMixin,
                           GenericViewSet):
    queryset = Entertainment.objects.all().prefetch_related('prices', 'photos')
    serializer_class = EntertainmentSerializer


@method_decorator(name='list', decorator=galery_schema.list())
class GaleryViewSet(mixins.ListModelMixin,
                           GenericViewSet):
    queryset = Galery.objects.all().prefetch_related('photos')
    serializer_class = GalerySerializer


@method_decorator(name='list', decorator=nearest_schema.list())
class NearestPlaceViewSet(mixins.ListModelMixin,
                          GenericViewSet):
    queryset = NearestPlace.objects.all().prefetch_related('photos')
    serializer_class = NearestPlaceSerializer
