from django import views
from django.shortcuts import redirect

from config.settings import FRONTEND_URL


def index_redirect(request):
    return redirect(FRONTEND_URL)