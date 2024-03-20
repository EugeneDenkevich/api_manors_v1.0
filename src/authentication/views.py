from django.utils.decorators import method_decorator
from rest_framework import viewsets
from .models import TelegramIdUser
from .schemas import telegram_schema
from .serializers import TelegramSerializer


@method_decorator(name="create", decorator=telegram_schema.create())
class TelegramModelViewSet(viewsets.ModelViewSet):
    queryset = TelegramIdUser.objects.all()
    serializer_class = TelegramSerializer
    http_method_names = ["post"]
