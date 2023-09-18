from rest_framework.serializers import (
    Serializer,
    ListSerializer,
    ModelSerializer,
    PrimaryKeyRelatedField,
    CharField,
    IntegerField,
    FileField,
    SerializerMethodField,
)
from rest_framework.exceptions import ValidationError

from .models import (
    Object,
    PhotoObject,
    ObjectFeature,
    FEATURES_CHOICES,
    Purchase,
)


class FileListSerializer(ListSerializer):
    child = FileField()

    def to_representation(self, instance):
        photos = instance.instance.photos.all()
        request = self.context.get('request')
        return list(request.build_absolute_uri(photo.file.url) for photo in photos)
    

class TypesSerializer(Serializer):
    id = IntegerField(required=False)
    type = CharField(required=False)
    count = IntegerField(required=False)


class ObjectPhotoSerializer(ModelSerializer):
    class Meta:
        model = PhotoObject
        fields = ['file',]

    def to_representation(self, instance):
        res = super().to_representation(instance)
        return res['file']


class ObjectFeaturesSerializer(ModelSerializer):
    id = SerializerMethodField()

    class Meta:
        model = ObjectFeature
        fields = [
            'id',
            'type'
        ]

    def get_id(self, obj):
        for i in range(len(FEATURES_CHOICES)):
            if FEATURES_CHOICES[i][0] == obj.type:
                return i + 1


class ObjectSerializer(ModelSerializer):
    photos = FileListSerializer(required=False)
    features = ObjectFeaturesSerializer(many=True, required=False)
    bed_count = IntegerField(required=False)
    beds_types = ListSerializer(child=TypesSerializer(), required=False, read_only=True)
    rooms_types = ListSerializer(child=TypesSerializer(), required=False, read_only=True)

    class Meta:
        model = Object
        exclude = [
            'created_date',
            'is_reserved'
        ]


class PurchaseSerializer(ModelSerializer):
    object = PrimaryKeyRelatedField(queryset=Object.objects.all())

    class Meta:
        model = Purchase
        exclude = [
            'status',
            'is_finished',
            'was_object',
            'stat',
        ]        
 
    def validate(self, data):
        """
        Check if desired arrival lower than desired departure
        """
        if data.get('desired_arrival') > data.get('desired_departure'):
            raise ValidationError(
                {'desired_departure': 'The departure date should be later than the arrival date.'}, 400
            )
        return data
