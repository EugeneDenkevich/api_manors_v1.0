from rest_framework import viewsets
from django.db.models import Count
from django.utils.decorators import method_decorator

from object.logic import get_beds_and_rooms
from object.models import Object
from object.models import Purchase
from object.serializers import ObjectSerializer
from object.serializers import PurchaseSerializer
from object.schemas import house_schema
from object.schemas import purchase_schema


@method_decorator(name='retrieve', decorator=house_schema.retrieve())
@method_decorator(name='list', decorator=house_schema.list())
class ObjectModelViewSet(viewsets.ModelViewSet):
    queryset = Object.objects.all().prefetch_related('photos', 'features').annotate(
        bed_count=Count('beds')
    )
    serializer_class = ObjectSerializer
    http_method_names = ['get']

    def retrieve(self, request, *args, **kwargs):
        response = super().retrieve(request, *args, **kwargs)
        response.data = get_beds_and_rooms(response.data)
        return response

    def list(self, request, *args, **kwargs):
        """
        Append beds_types and rooms_types by 2 query
        instead of the whole list of COUNT(*) query
        """
        response = super().list(request, *args, **kwargs)
        response.data = get_beds_and_rooms(response.data)
        return response


@method_decorator(name='create', decorator=purchase_schema.create())
class PurchaseModelViewSet(viewsets.ModelViewSet):
    queryset = Purchase.objects.all()
    serializer_class = PurchaseSerializer
    http_method_names = ['post']
