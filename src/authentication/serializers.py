from .models import TelegramIdUser
from rest_framework.serializers import ModelSerializer, PrimaryKeyRelatedField


class TelegramSerializer(ModelSerializer):
    class Meta:
        model = TelegramIdUser
        fields = "__all__"
