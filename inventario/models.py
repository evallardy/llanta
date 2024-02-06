from django.contrib.auth.mixins import PermissionRequiredMixin
from django.db import models

# Create your models here.

class Llanta(models.Model, PermissionRequiredMixin):
    # Generales
    producto_clave = models.CharField("Producto/Clave",max_length=100, blank=True, null=True)
    descripcion = models.CharField("Descripción", max_length=255, blank=True, null=True)
    existencia = models.IntegerField("Existencia", default=0)
    precio = models.DecimalField("Costo Promedio Pesos", decimal_places=2, max_digits=10, default=0)
    # Especificación
    ancho = models.CharField("Ancho",max_length=10, blank=True, null=True)
    alto = models.CharField("Alto",max_length=10, blank=True, null=True)
    rin = models.CharField("Rin",max_length=10, blank=True, null=True)
    marca = models.CharField("Marca",max_length=100, blank=True, null=True)
    # Bitácora
    creado = models.DateTimeField("Creado", auto_now_add=True)
    modificado = models.DateTimeField("Actualizado", auto_now=True)


    class Meta:
        verbose_name = 'Llanta' 
        verbose_name_plural = 'Llantas'
        ordering = ['producto_clave']
        unique_together = [['producto_clave']]
        db_table = 'Llanta'
