from rest_framework import serializers
from rest_framework.serializers import (
    ListSerializer,
    ModelSerializer,
    FileField,
)

from .models import (
    EntertainmentPrice,
    Entertainment,
    NearestPlace,
    Galery,
)


class FileListSerializer(ListSerializer):
    child = FileField()

    def to_representation(self, instance):
        photos = instance.instance.photos.all()
        request = self.context.get('request')
        if request:
            return list(request.build_absolute_uri(photo.file.url) for photo in photos)


class EntertainmentPriceSerializer(ModelSerializer):
    service_name = serializers.CharField()

    class Meta:
        model = EntertainmentPrice
        fields = ['service_name']

    def to_representation(self, instance):
        return {instance.header: instance.price}


class EntertainmentSerializer(ModelSerializer):
    prices = EntertainmentPriceSerializer(many=True, required=False)
    photos = FileListSerializer(required=False)

    class Meta:
        model = Entertainment
        fields = '__all__'


class NearestPlaceSerializer(ModelSerializer):
    photos = FileListSerializer(required=False)

    class Meta:
        model = NearestPlace
        fields = '__all__'


class GalerySerializer(ModelSerializer):
    photos = FileListSerializer(required=False)

    class Meta:
        model = Galery
        fields = '__all__'
