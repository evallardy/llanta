from django.urls import path

from .views import index

urlpatterns = [
    path('cotizacion/<cliente_info>/', FormatocotizacionHTMLaPDF.as_view(), name='cotizacion_formato'),
]