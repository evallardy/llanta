from django.urls import path, include

from .views import *

urlpatterns = [
    path('archivo/', Importa_archivo.as_view(), name='importa_archivo'),
]
