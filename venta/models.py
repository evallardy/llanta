from django.contrib.auth.mixins import PermissionRequiredMixin
from django.db import models
from django.utils import timezone

# Create your models here.

class Cotizacion(models.Model, PermissionRequiredMixin):
    # Generales
    cliente = models.CharField("Cliente", max_length=80)
    producto_clave = models.CharField("Producto/Clave",max_length=100)
    descripcion = models.CharField("Descripción", max_length=255)
    existencia = models.IntegerField("Existencia", default=0)
    solicita = models.IntegerField("Solicita", default=0)
    precio = models.DecimalField("Precio", decimal_places=2, max_digits=10, default=0)
    total = models.DecimalField("Total", decimal_places=2, max_digits=10, default=0)
    correo_electronico = models.EmailField("Correo Electrónico", max_length=254, null=True, blank=True)
    # Bitácora
    vigencia = models.DateTimeField("Vigencia", default=timezone.now() + timezone.timedelta(days=60))
    creado = models.DateTimeField("Creado", auto_now_add=True)
    modificado = models.DateTimeField("Actualizado", auto_now=True)


    class Meta:
        verbose_name = 'Cotización' 
        verbose_name_plural = 'Cotizaciones' 
        ordering = ['cliente','-creado']
        db_table = 'Cotizacion'
