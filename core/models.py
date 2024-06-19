from django.contrib.auth.mixins import PermissionRequiredMixin
from django.db import models
from django.utils import timezone
from datetime import timedelta

AMBITO = (
    (1, 'toda la tienda'),
    (2, 'Familia'),
    (3, 'Familia Subfamilia'),
    (4, 'Producto'),
)
CVE_PROMOCION = (
    (1, 'Meses sin intereses'),
    (2, 'Meses con intereses'),
    (3, 'Descuento en pago en efectivo'),
    (4, 'Llevate X y pago Y'),
)
ESTATUS_MENSAJE = (
    (0, 'Terminado'),
    (1, 'Activo'),
)
TIPO_VALOR = (
    (1, 'Porcentaje'),
    (2, 'Importe'),
    (3, 'Cantidad'),
)

def default_vigencia_fin():
    return timezone.now() + timedelta(days=30)
class Llanta(models.Model, PermissionRequiredMixin):
    # Datos extraídos
    producto_clave = models.CharField("Producto/Clave",max_length=100, blank=True, null=True)
    descripcion = models.CharField("Descripción", max_length=255, blank=True, null=True)
    existencia = models.IntegerField("Existencia", default=0)
    costo_promedio_pesos = models.DecimalField("Costo Promedio Pesos", decimal_places=2, max_digits=10, default=0)
    tipo = models.CharField("Tipo",max_length=50, blank=True, null=True)
    subtipo = models.CharField("Subtipo",max_length=50, blank=True, null=True)
    capas = models.IntegerField("Capas", default=0)
    precio_especia_llantashop_pago_efectivo = models.DecimalField("Precio Especia LLANTASHOP pago Efectivo", decimal_places=2, max_digits=10, default=0)
    msi_3 = models.DecimalField("3 MSI", decimal_places=2, max_digits=10, default=0)
    msi_6 = models.DecimalField("6 MSI", decimal_places=2, max_digits=10, default=0)
    msi_9 = models.DecimalField("9 MSI", decimal_places=2, max_digits=10, default=0)
    msi_12 = models.DecimalField("12 MSI", decimal_places=2, max_digits=10, default=0)
    msi_18 = models.DecimalField("18 MSI", decimal_places=2, max_digits=10, default=0)
    envio = models.DecimalField("Envio", decimal_places=2, max_digits=10, default=0)
    utilidad = models.DecimalField("Utilidad", decimal_places=2, max_digits=10, default=0)
    afiliado = models.DecimalField("Afiliado", decimal_places=2, max_digits=10, default=0)
    actualizado = models.IntegerField("Actualizado en el proceso de extracción", default=1)
    # Datos separados
    ancho = models.CharField("Ancho",max_length=10, blank=True, null=True)
    alto = models.CharField("Alto",max_length=10, blank=True, null=True)
    rin = models.CharField("Rin",max_length=10, blank=True, null=True)
    radial = models.IntegerField("Radial", default=0)
    marca = models.CharField("Marca",max_length=100, blank=True, null=True)
    # Bitácora
    creado = models.DateTimeField("Creado", auto_now_add=True)
    modificado = models.DateTimeField("Actualizado", auto_now=True)


    class Meta:
        verbose_name = 'Llanta' 
        verbose_name_plural = 'Llantas' 
        ordering = ['producto_clave']
        db_table = 'Llanta'
class MensajePicky(models.Model, PermissionRequiredMixin):
    token = models.CharField("Token", max_length=255, null=True, blank=True)
    number = models.CharField("Number", max_length=50)                                 # Number
    message_in = models.CharField("Mensage in", max_length=255)                        # Message_in
    message_in_raw = models.CharField("Mensaje in raw", max_length=255)                # Message_in_raw
    message = models.CharField("Mensaje", max_length=255, null=True, blank=True)
    application = models.CharField("Aplicación", max_length=255, null=True, blank=True)# Application
    tipo = models.CharField("Type", max_length=255, default=2)                         # Tipo 
    unique_id = models.CharField("Unique id", max_length=255, null=True, blank=True)
    quoted = models.CharField("Quoted", max_length=255, null=True, blank=True)
    estatus_mensaje = models.IntegerField("Estatus del mensaje", choices=ESTATUS_MENSAJE, default=1)
    nivel = models.IntegerField("Nivel de pregunta", default=1)
    opcion1 = models.JSONField("Acción", null=True, blank=True)
    opcion2 = models.JSONField("Bien", null=True, blank=True)
    opcion3 = models.JSONField("Estado", null=True, blank=True)
    opcion4 = models.JSONField("Municipio", null=True, blank=True)
    opcion5 = models.JSONField("Bien seleccionado", null=True, blank=True)
    # Bitácora
    creado = models.DateTimeField("Creado", default=timezone.now)
    modificado = models.DateTimeField("Actualizado", auto_now=True)

    class Meta:
        verbose_name = 'Mensaje picky'
        verbose_name_plural = 'Mensajes picky'
        ordering = ['number','-creado',]
        db_table = 'MensajePicky'

    def __str__(self):
        return '%s %s' % (self.number, self.message_in)

class Bitacora(models.Model, PermissionRequiredMixin):
    descripcion = models.CharField("Descripción", max_length=255)
    # Bitácora
    creado = models.DateTimeField("Creado", default=timezone.now)
    modificado = models.DateTimeField("Actualizado", auto_now=True)
    
    class Meta:
        verbose_name = 'Registro'
        verbose_name_plural = 'Registros'
        ordering = ['-creado']
        db_table = 'Bitcora'
    
    def __str__(self):
        return '%s - %s' % (self.fecha, self.descripcion)

class Familia(models.Model, PermissionRequiredMixin):
    familia = models.CharField("Familia",max_length=100)
    idSubfamilia = models.IntegerField('Id Subfamilia', default=0)
    subFamilia = models.CharField("Subfamilia",max_length=100)
    # Bitácora
    creado = models.DateTimeField("Creado", auto_now_add=True)
    modificado = models.DateTimeField("Actualizado", auto_now=True)

    class Meta:
        verbose_name = 'Familia'
        verbose_name_plural = 'Familias'
        ordering = ['familia', 'subFamilia']
        db_table = 'Familia'
    
    def __str__(self):
        return '%s / %s' % (self.familia, self.subFamilia)

class Empresa(models.Model, PermissionRequiredMixin):
    razon = models.CharField("Razon",max_length=100)
    giro = models.CharField("Giro",max_length=100)
    # Nombre de caracteristicas del producto
    esquema = models.JSONField('Esquema')
    # Bitácora
    creado = models.DateTimeField("Creado", auto_now_add=True)
    modificado = models.DateTimeField("Actualizado", auto_now=True)

    class Meta:
        verbose_name = 'Empresa' 
        verbose_name_plural = 'Empresas' 
        ordering = ['razon']
        db_table = 'Empresa'

    def __str__(self):
        return '%s - %s' % (self.razon, self.giro)

class Producto(models.Model, PermissionRequiredMixin):
    producto_clave = models.CharField("Producto/Clave",max_length=100, blank=True, null=True)
    descripcion = models.CharField("Descripción", max_length=255, blank=True, null=True)
    existencia = models.IntegerField("Existencia", default=0)
    costo = models.DecimalField("Costo", decimal_places=2, max_digits=10, default=0)
    precio = models.DecimalField("Precio", decimal_places=2, max_digits=10, default=0)
    familia = models.ForeignKey(Familia, on_delete=models.CASCADE, related_name="ProdFam",
        blank=True, null=True)
    subFamilia = models.ForeignKey(Familia, on_delete=models.CASCADE, related_name="ProdSFam",
        blank=True, null=True)
    caracteristicas = models.JSONField("Caracteristicas", blank=True, null=True)
    # Bitácora
    creado = models.DateTimeField("Creado", auto_now_add=True)
    modificado = models.DateTimeField("Actualizado", auto_now=True)

    class Meta:
        verbose_name = 'Producto' 
        verbose_name_plural = 'Productos' 
        ordering = ['producto_clave']
        db_table = 'Producto'

    def __str__(self):
        return '%s' % (self.descripcion)

class CaracProm(models.Model, PermissionRequiredMixin):
    #    AMBITO
    # 1 toda la tienda
    # 2 Familia
    # 3 Familia Subfamilia
    # 4 Producto 
    ambito = models.IntegerField("Ámbito", choices=AMBITO, default=4)
    familia = models.ForeignKey(Familia, on_delete=models.CASCADE, related_name="caracPromFam",
        blank=True, null=True)
    subFamilia = models.ForeignKey(Familia, on_delete=models.CASCADE, related_name="caracPromSFam",
        blank=True, null=True)
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE, related_name="caracPromProd",
        blank=True, null=True)
    #    PROMOCION
    # 1 Meses sin intereses
    # 2 Meses con intereses
    # 3 Descuento en pago en efectivo
    # 4 Llevate X y pago Y
    cveProm = models.IntegerField("Cve. Promocion", choices=CVE_PROMOCION, default=4)
    descProm = models.CharField('Descripción promoción', max_length=255)
    #    TIPO
    # 1 Porcentaje valor1
    # 2 Importe    valor1
    # 3 Cantidad   valor1 y paga valor2
    tipo = models.IntegerField("Cve. Promocion", choices=TIPO_VALOR, default=4)
    valor1 = models.DecimalField("Valor 1", max_digits=8, decimal_places=2, default=0)
    valor2 = models.DecimalField("Valor 2", max_digits=8, decimal_places=2, default=0)
    vigenciaInicio = models.DateField("Inicio vigencia", default=timezone.now)
    vigenciaFin = models.DateField("Fin vigencia", default=default_vigencia_fin)
    # Bitácora
    creado = models.DateTimeField("Creado", auto_now_add=True)
    modificado = models.DateTimeField("Actualizado", auto_now=True)
    
    class Meta:
        verbose_name = 'Caracterica pago' 
        verbose_name_plural = 'Caracteristicas pago' 
        ordering = ['ambito','cveProm']
        db_table = 'CaracProd'

    def __str__(self):
        return '%s' % (self.get_ambito_display, cveProm)

'''
    # Datos separados
    ancho = models.CharField("Ancho",max_length=10, blank=True, null=True)
    alto = models.CharField("Alto",max_length=10, blank=True, null=True)
    rin = models.CharField("Rin",max_length=10, blank=True, null=True)
    radial = models.IntegerField("Radial", default=0)
    marca = models.CharField("Marca",max_length=100, blank=True, null=True)
'''