from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView

from config import views
from object.views import *
from .views import bot_view


urlpatterns = [

    # Index redirect
    path('', views.index_redirect, name='index'),

    # Doc
    path('schema/', SpectacularAPIView.as_view(), name='schema'),
    path('swagger-ui/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),   

    # API
  
    path('api/', include('object.urls')),
    path('api/', include('entertainments.urls')),
    path('api/', include('info.urls')),
    path('api/', include('pages.urls')),

    # Admin
    path('admin/', admin.site.urls),

    # Bot
    path(f'bot/{settings.BOT_TOKEN}', bot_view, name="bot"),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)
    