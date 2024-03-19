from django.utils.decorators import method_decorator
from rest_framework import viewsets
from .models import TelegramIdUser
from .schemas import TelegramSchema
from .serializers import TelegramSerializer


@method_decorator(name='owner', decorator=TelegramSchema.create())
class TelegramModelViewSet(viewsets.ModelViewSet):
    queryset = TelegramIdUser.objects.all()
    serializer_class = TelegramSerializer
