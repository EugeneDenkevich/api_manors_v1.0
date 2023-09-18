from rest_framework.serializers import (
    ListSerializer,
    ModelSerializer,
    FileField,
)

from .models import (
    MainPage,
    PolicyAgreement,
    BackPhoto
)

class FileListSerializer(ListSerializer):
    child = FileField()

    def to_representation(self, instance):
        photos = instance.instance.photos.all()
        request = self.context.get('request')
        return list(request.build_absolute_uri(photo.file.url) for photo in photos)


class MainPageModelSerializer(ModelSerializer):
    photos = FileListSerializer()

    class Meta:
        model = MainPage
        exclude = ['id', 'was_changed']


class BackPhotoSerializer(ModelSerializer):
    class Meta:
        model = BackPhoto
        exclude = ['id', 'was_changed']


class PolicyAgreementsSerializer(ModelSerializer):
    class Meta:
        model = PolicyAgreement
        exclude = ['id', 'was_changed']
