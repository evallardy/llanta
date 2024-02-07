from django.urls import path

from .api import mensaje

urlpatterns = [
    path('', mensaje_whatsapp, name = 'mensaje_whatsapp'),
]