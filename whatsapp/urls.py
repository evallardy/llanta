from django.urls import path

from .api import mensaje_whatsapp

urlpatterns = [
    path('', mensaje_whatsapp, name = 'mensaje_whatsapp'),
]