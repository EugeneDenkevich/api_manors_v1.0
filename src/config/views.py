from django.shortcuts import redirect
from drf_spectacular.utils import extend_schema
from rest_framework.response import Response
from rest_framework.request import Request
from rest_framework.decorators import api_view
from django.views.decorators.csrf import csrf_exempt
from rest_framework import status

from config.settings import FRONT_DOMAIN


def index_redirect(request):
    return redirect("https://" + FRONT_DOMAIN)


@extend_schema(
    tags=["Bot"],
    description='Bot webhook',
    summary='Bot webhook', 
)
@api_view(["POST"])
@csrf_exempt
def bot_view(request: Request):
    """Установка вебхука для бота"""
    # TODO Сделать установку вебхука.
    message = dict(request.data)
    chat = message["chat"]
    chat_id = int(chat[chat.index("id") + 1])
    print(chat_id)
    return Response({"detail": "success"}, status=status.HTTP_200_OK)
