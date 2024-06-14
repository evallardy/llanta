from django.contrib import admin
from django.urls import path, re_path
from django.conf import settings
from django.views.static import serve
from django.conf.urls.static import static
from django.urls.conf import include
from django.urls import path

from core.api import mensaje_api_view

urlpatterns = [
    path('', mensaje_api_view, name = 'mensajes_api_picky'),
]