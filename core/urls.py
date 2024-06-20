from django.contrib import admin
from django.urls import path, re_path
from django.conf import settings
from django.views.static import serve
from django.conf.urls.static import static
from django.urls.conf import include
from django.urls import path

from core.api import mensaje_api_view
from .views import politicas, suscripcion_view

urlpatterns = [
    path('', mensaje_api_view, name = 'mensajes_api_picky'),
    path('politicas/', politicas, name='politicas'),
    path('suscripcion_view/', suscripcion_view, name='suscripcion_view'),
    
]