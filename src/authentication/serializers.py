from .models import TelegramIdUser
from rest_framework.serializers import ModelSerializer, PrimaryKeyRelatedField


class TelegramSerializer(ModelSerializer):
    telegram_id = PrimaryKeyRelatedField(queryset=TelegramIdUser.objects.all())
