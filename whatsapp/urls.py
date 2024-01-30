from django.urls import path

from .api import mensaje

urlpatterns = [
    path('', mensaje, name = 'mensaje'),
]