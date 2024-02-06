from xhtml2pdf import pisa
import os
from django.template.loader import get_template
from django.http import HttpResponse
from django.shortcuts import render
from django.conf import settings
from django.utils import timezone
from django.core.mail import EmailMessage

from venta.models import Cotizacion

class FormatocotizacionHTMLaPDF:
    #    def get(self, request, *args, **kwargs):
    def generar_remision_pdf(request, datos):

        cliente = datos.get('cliente')
        producto_clave = datos.get('producto_clave')
        descripcion = datos.get('descripcion')
        existencia = int(datos.get('existencia'))
        solicita = datos.get('solicita')
        precio = datos.get('precio')
        total = datos.get('total')
        correo_electronico = datos.get('correo_electronico')

        cotizacion = Cotizacion(
            cliente = cliente,
            producto_clave = producto_clave,
            descripcion = descripcion,
            existencia = existencia,
            solicita = solicita,
            precio = precio,
            total = total,
            correo_electronico = correo_electronico
        )

        cotizacion.save()

        # Calcular el total y agregar información adicional
        numero_cotizacion = cotizacion.id
        fecha_entrega = cotizacion.creado
        total = cotizacion.total
        vigencia = cotizacion.vigencia

        # Renderizar la plantilla HTML
        template = get_template('venta/cotizacionPDF.html')
        context = {
            'numero_cotizacion' : numero_cotizacion,
            'fecha_entrega' : fecha_entrega,
            'vigencia' : vigencia,
            'cliente' : cliente,
            'producto_clave' : producto_clave,
            'descripcion' : descripcion,
            'existencia' : existencia,
            'solicita' : solicita,
            'precio' : precio,
            'total' : total,
        }
        html = template.render(context)

        # Convertir la plantilla HTML a PDF
        pdf_response = HttpResponse(content_type='application/pdf')
        pdf_response['Content-Disposition'] = f'attachment; filename="remision_{numero_cotizacion}.pdf"'
        pisa.CreatePDF(html, dest=pdf_response)

        # Obtén la ruta de la carpeta del cliente
        carpeta_cliente = os.path.join(settings.ARCHIVOS_REMISIONES_DIR, f'cliente_{cliente}')

        # Crea la carpeta del cliente si no existe
        os.makedirs(carpeta_cliente, exist_ok=True)

        # Obtén la ruta completa del archivo PDF
        ruta_pdf = os.path.join(carpeta_cliente, f'remision_{numero_cotizacion}.pdf')

        # Guardar el PDF en la carpeta del cliente
        with open(ruta_pdf, 'wb') as pdf_file:
            pdf_file.write(pdf_response.getvalue())

        return ruta_pdf

    def envia_correo(request, archivo, correo_electronico):

        # Crea el objeto EmailMessage
        mensaje = EmailMessage(
            'Prueba Asunto del Correo',  # Asunto del correo
            'Cuerpo del Correo',  # Cuerpo del correo (puede estar en formato HTML)
            'evallardy@gmail.com',  # Correo del remitente
            [correo_electronico],  # Lista de destinatarios
        )

        # Adjunta el archivo PDF al correo
        mensaje.attach_file(archivo)

        # Envía el correo
        mensaje.send()

        # Opcionalmente, puedes eliminar el archivo PDF después de enviar el correo si no lo necesitas más
        # os.remove(ruta_pdf)
