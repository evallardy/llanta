from django.contrib.auth.mixins import PermissionRequiredMixin
from django.db import models

# Create your models here.

ESTATUS_MENSAJE = (
    (0, 'Terminado'),
    (1, 'Activo'),
)

