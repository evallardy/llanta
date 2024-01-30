from django.contrib.auth.mixins import PermissionRequiredMixin
from django.db import models

from core.models import ESTATUS_MENSAJE

# Create your models here.

class MensajePicky(models.Model, PermissionRequiredMixin):
    token = models.CharField("Token", max_length=255, null=True, blank=True)
    number = models.CharField("Number", max_length=50)
    message_in = models.CharField("Mensage in", max_length=255)
    message_in_raw = models.CharField("Mensaje in raw", max_length=255)
    message = models.CharField("Mensaje", max_length=255, null=True, blank=True)
    application = models.CharField("Aplicación", max_length=255, null=True, blank=True)
    tipo = models.CharField("Type", max_length=255, default=2)
    unique_id = models.CharField("Unique id", max_length=255, null=True, blank=True)
    quoted = models.CharField("Quoted", max_length=255, null=True, blank=True)
    estatus_mensaje = models.IntegerField("Estatus del mensaje", choices=ESTATUS_MENSAJE, default=1)
    fecha_alta = models.DateTimeField("Fecha alta", auto_now_add=True)
    nivel = models.IntegerField("Nivel de pregunta", default=1)
    opcion1 = models.JSONField("Bienvenida", null=True, blank=True)
    opcion2 = models.JSONField("Ancho", null=True, blank=True)
    opcion3 = models.JSONField("Alto", null=True, blank=True)
    opcion4 = models.JSONField("Rin", null=True, blank=True)
    opcion5 = models.JSONField("Opciones", null=True, blank=True)

    class Meta:
        verbose_name = 'Mensaje picky'
        verbose_name_plural = 'Mensajes picky'
        ordering = ['number','-fecha_alta',]
        db_table = 'MensajePicky'

class Bitacora(models.Model, PermissionRequiredMixin):
    descripcion = models.CharField("Descripción", max_length=255)
    fecha = models.DateTimeField("Fecha", auto_now_add=True)
    
    class Meta:
        verbose_name = 'Registro'
        verbose_name_plural = 'Registros'
        ordering = ['-fecha']
        db_table = 'Bitcora'
    
    def __str__(self):
        return '%s - %s' % (self.fecha, self.descripcion)
