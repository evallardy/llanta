from django.shortcuts import render, redirect
import gspread
from google.auth import credentials
from google.auth.transport.requests import Request
from google.oauth2 import service_account
from django.views import View
from django.contrib import messages

from .models import *
from .forms import SuscripcionForm

def format_phone_number(phone_number):
    # Supongamos que el formato deseado es "+52 551-880-7850"
    if len(phone_number) == 12 and phone_number.startswith('52'):
        country_code = phone_number[:2]
        area_code = phone_number[2:5]
        first_part = phone_number[5:8]
        second_part = phone_number[8:]
        formatted_number = f"+{country_code} {area_code}-{first_part}-{second_part}"
        return formatted_number
    return phone_number

def separa_datos(request, clave, descripcion):
    separa_datos = {}
    campo = 0
    posicion = 0
    separa_datos['ancho'] = ""
    separa_datos['alto'] = ""
    separa_datos['rin'] = ""
    separa_datos['radial'] = ""
    separa_datos['marca'] = ""
    a = 0

    for letra in descripcion:
        posicion += 1
        if campo == 0:
            if letra == '/' or letra.upper() == 'X' or letra.upper() == 'R':
                posicion_final = posicion - 1
                separa_datos["ancho"] = descripcion[0:posicion_final]
                campo += 1
                posicion_inicial = posicion
            if letra.upper() == 'R':
                campo += 1
                separa_datos["alto"] = "0"
                separa_datos["radial"] = 1
        elif campo == 1:
            if letra.upper() == 'R' or letra == '-':
                posicion_final = posicion - 1
                separa_datos["alto"] = descripcion[posicion_inicial:posicion_final]
                posicion_inicial = posicion
                campo += 1
                separa_datos["radial"] = 0
                if letra.upper() == 'R':
                    separa_datos["radial"] = 1
        elif campo == 2:
            if letra == ' ':
                posicion_final = posicion - 1
                separa_datos["rin"] = descripcion[posicion_inicial:posicion_final]
                posicion_inicial = posicion
                campo += 1
        elif campo == 3:
                separa_datos["marca"] = descripcion[posicion_inicial:]
    return separa_datos

def leer(request):
    credenciales = "core/seg/arch/cve/desllantashop-8aaa1edf374f.json"
    scope = ['https://www.googleapis.com/auth/spreadsheets']
    credenciales = service_account.Credentials.from_service_account_file(credenciales, scopes=scope)
    cliente = gspread.authorize(credenciales)
    hoja = cliente.open_by_key('1F04sEKIe7O8b2MH_Ib6OP31DEguhvJZdiHu_gZzLBno')
    hoja_especifica = hoja.get_worksheet(0)
    datos = hoja_especifica.get_all_records()
    limpia = Llanta.objects.filter(producto_clave__gt="").update(actualizado=0)
    nuevos = 0
    actualizados = 0
    duplicados = 0
    errores = 0
    sin_modificacion = 0
    total = 0
    registros_duplicados = []
    for registro in datos:
        llanta = {}
        registro_completo = {}
        actualiza = None
        nuevo_registro = None
        total += 1
        for key, value in registro.items():
            llanta['actualizado'] = 1
            registro_completo['actualizado'] = 0
            if key == "Producto/Clave":
                producto_clave = value
                registro_completo['producto_clave'] = value
            elif key == "Descripción":
                descripcion = value
                registro_completo['descripcion'] = value
            elif key == "Existencia":
                llanta['existencia'] = value
                registro_completo['existencia'] = value
            elif key == "Costo Promedio Pesos":
                llanta['costo_promedio_pesos'] = value.replace(',', '').replace('$','')
                registro_completo['costo_promedio_pesos'] = value.replace(',', '').replace('$','')
            elif key == "Tipo":
                llanta['tipo'] = value
                registro_completo['tipo'] = value
            elif key == "Subtipo":
                llanta['subtipo'] = value
                registro_completo['subtipo'] = value
            elif key == "Capas":
                llanta['capas'] = value
                registro_completo['capas'] = value
            elif key == "Precio Especia LLANTASHOP pago Efectivo":
                llanta['precio_especia_llantashop_pago_efectivo'] = value.replace(',', '').replace('$','')
                registro_completo['precio_especia_llantashop_pago_efectivo'] = value.replace(',', '').replace('$','')
            elif key == "3 MSI":
                llanta['msi_3'] = value.replace(',', '').replace('$','')
                registro_completo['msi_3'] = value.replace(',', '').replace('$','')
            elif key == "6 MSI":
                llanta['msi_6'] = value.replace(',', '').replace('$','')
                registro_completo['msi_6'] = value.replace(',', '').replace('$','')
            elif key == "9 MSI":
                llanta['msi_9'] = value.replace(',', '').replace('$','')
                registro_completo['msi_9'] = value.replace(',', '').replace('$','')
            elif key == "12 MSI":
                llanta['msi_12'] = value.replace(',', '').replace('$','')
                registro_completo['msi_12'] = value.replace(',', '').replace('$','')
            elif key == "18 MSI":
                llanta['msi_18'] = value.replace(',', '').replace('$','')
                registro_completo['msi_18'] = value.replace(',', '').replace('$','')
            elif key == "ENVIO":
                llanta['envio'] = value.replace(',', '').replace('$','')
                registro_completo['envio'] = value.replace(',', '').replace('$','')
            elif key == "UTILIDAD":
                llanta['utilidad'] = value.replace(',', '').replace('$','')
                registro_completo['utilidad'] = value.replace(',', '').replace('$','')
            elif key == "AFILIADO":
                llanta['afiliado'] = value.replace(',', '').replace('$','')
                registro_completo['afiliado'] = value.replace(',', '').replace('$','')

        datos_creados = separa_datos(request, producto_clave, descripcion)
        registro_completo['ancho'] = datos_creados['ancho']
        registro_completo['alto'] = datos_creados['alto']
        registro_completo['rin'] = datos_creados['rin']
        registro_completo['radial'] = datos_creados['radial']
        registro_completo['marca'] = datos_creados['marca']
        llanta['ancho'] = datos_creados['ancho']
        llanta['alto'] = datos_creados['alto']
        llanta['rin'] = datos_creados['rin']
        llanta['radial'] = datos_creados['radial']
        llanta['marca'] = datos_creados['marca']
        registro_existente = Llanta.objects.filter(producto_clave=producto_clave, descripcion=descripcion).first()
        if registro_existente:
            if registro_existente.actualizado == 0:
                registro_igual = Llanta.objects.filter(**registro_completo).first()                
                if registro_igual:
                    Llanta.objects.filter(**registro_completo).update(actualizado=1)                
                    sin_modificacion += 1
                else:
                    actualiza = Llanta.objects.filter(producto_clave=producto_clave, descripcion=descripcion).update(**llanta)
                    actualizados += 1
            else:
                duplicados += 1
                registro = {'consec': duplicados, 'clave': producto_clave, 'descripcion': descripcion}
                registros_duplicados.append(registro)
        else:
            llanta['producto_clave'] = producto_clave
            llanta['descripcion'] = descripcion
            nuevo_registro = Llanta(**llanta)
            nuevo_registro.save()
            nuevos += 1
    eliminados = Llanta.objects.filter(actualizado = 0).delete()
 #   print('Nuevos ' + str(nuevos))
 #   print('Actualizados ' + str(actualizados))
 #   print('Duplicados ' + str(duplicados))
 #   print('Sin modificación ' + str(sin_modificacion))
 #   print('Total de registros leidos ' + str(total))
 #   print('Eliminados ' + str(eliminados[0]))
    resultado = {}
    resultado['Nuevos'] = nuevos
    resultado['Actualizados '] = actualizados
    resultado['Duplicados'] = duplicados
    resultado['Sin modificación'] = sin_modificacion
    resultado['Total de registros leidos'] = total
    resultado['Eliminados'] = eliminados[0]
    resultado['registros_duplicados'] = registros_duplicados
    return resultado

def empresa():
    context = {}
    context['titulo'] = 'Llantabot'
    context['descripcion'] = 'Tu asistente virtual para la venta de llantas.'
    context['currentURL'] = 'https://llantabot.com'
    telefono_cliente = '525518807850'
    context['PHONE_NUMBER'] = telefono_cliente
    context['PHONE_NUMBER_FRM'] = format_phone_number(telefono_cliente)
    return context


class Index(View):
    template_name = 'core/index.html'
    def get(self, request, *args, **kwargs):
        context = {}
        context['index_active'] = True
        context['empresa'] = empresa()
        return render(request, self.template_name, context)

def politicas(request):
    context = {}
    context['empresa'] = empresa()
    return render(request, 'core/politicas.html', context)
class Politicas(View):
    template_name = 'core/politicas.html'

def suscripcion_view(request):
    if request.method == 'POST':
        form = SuscripcionForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "¡Suscripción realizada con éxito!")
            return redirect('index')  # Cambia 'success' por la URL de tu página de éxito
        else:
            messages.error(request, "")
            return render(request, 'core/index.html', {'form': form})
    return redirect('index')

'''
def index(request):
    template_name = 'core/index.html'
    context = {}
    if request.method == 'POST':
        datos = leer(request)
        context['datos'] = datos
    else:
        context['titulo'] = 'Llantabot'
        context['descripcion'] = 'Tu asistente virtual para la venta de llantas.'
        context['currentURL'] = 'https://llantabot.com'
    return render(request, template_name, context=context)
'''
