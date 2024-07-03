from django.contrib import admin
from django.urls import path, re_path
from django.conf import settings
from django.views.static import serve
from django.conf.urls.static import static
from django.urls.conf import include
from django.urls import path

from core.api import mensaje_api_view
from .views import politicas, suscripcion_view, \
    PromocionListView, PromocionDetailView, PromocionCreateView, \
    PromocionUpdateView, PromocionDeleteView, DetalleListView, \
    DetalleDetailView, DetalleCreateView, DetalleUpdateView, \
    DetalleDeleteView, PromocionDetalleListView, PromocionDetalleDetailView, \
    PromocionDetalleCreateView, PromocionDetalleUpdateView, \
    PromocionDetalleDeleteView, LoginCView, logoutC_view, Promociones

urlpatterns = [
    path('', mensaje_api_view, name = 'mensajes_api_picky'),
    path('politicas/', politicas, name='politicas'),
    path('promociones/', Promociones.as_view(), name='promociones'),
    path('suscripcion_view/', suscripcion_view, name='suscripcion_view'),

    path('loginC/', LoginCView.as_view(), name='loginC'),
     path('logoutC/', logoutC_view, name='logoutC'),

    path('promociones/', PromocionListView.as_view(), name='promocion_list'),
    path('promociones/<int:pk>/', PromocionDetailView.as_view(), name='promocion_detail'),
    path('promociones/crear/', PromocionCreateView.as_view(), name='promocion_create'),
    path('promociones/<int:pk>/editar/', PromocionUpdateView.as_view(), name='promocion_update'),
    path('promociones/<int:pk>/eliminar/', PromocionDeleteView.as_view(), name='promocion_delete'),

    # Detalle URLs
    path('detalles/', DetalleListView.as_view(), name='detalle_list'),
    path('detalles/<int:pk>/', DetalleDetailView.as_view(), name='detalle_detail'),
    path('detalles/crear/', DetalleCreateView.as_view(), name='detalle_create'),
    path('detalles/<int:pk>/editar/', DetalleUpdateView.as_view(), name='detalle_update'),
    path('detalles/<int:pk>/eliminar/', DetalleDeleteView.as_view(), name='detalle_delete'),

    # PromocionDetalle URLs
    path('promociondetalles/', PromocionDetalleListView.as_view(), name='promociondetalle_list'),
    path('promociondetalles/<int:pk>/', PromocionDetalleDetailView.as_view(), name='promociondetalle_detail'),
    path('promociondetalles/crear/', PromocionDetalleCreateView.as_view(), name='promociondetalle_create'),
    path('promociondetalles/<int:pk>/editar/', PromocionDetalleUpdateView.as_view(), name='promociondetalle_update'),
    path('promociondetalles/<int:pk>/eliminar/', PromocionDetalleDeleteView.as_view(), name='promociondetalle_delete'),
]