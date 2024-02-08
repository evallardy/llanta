from django.urls import path

from .api import mensaje_whatsapps

urlpatterns = [
    path('', mensaje_whatsapps, name = 'mensaje_whatsapps'),
]