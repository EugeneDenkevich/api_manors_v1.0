from django.utils.decorators import method_decorator
from rest_framework import viewsets, status
from rest_framework.response import Response
from .models import TelegramIdUser
from .schemas import telegram_schema
from .serializers import TelegramSerializer

from object.services import purchase_service
from object.services import purchase_service
from bot.services import bot_service
from authentication.service import telegram_service
from rest_framework.decorators import action


@method_decorator(name="create", decorator=telegram_schema.create())
class TelegramModelViewSet(viewsets.ModelViewSet):
    queryset = TelegramIdUser.objects.all()
    serializer_class = TelegramSerializer
    http_method_names = ["post", "get"]

    @telegram_schema.get_daily_data()
    @action(methods=["get"], detail=False, serializer_class=None)
    def get_daily_data(self, request) -> None:
        daily_data = purchase_service.get_daily_data()
        daily_data["telegram_ids"] = telegram_service.get_telegram_ids()
        return Response(data=daily_data, status=status.HTTP_200_OK)
