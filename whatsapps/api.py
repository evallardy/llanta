from rest_framework.response import Response
from django.http.response import HttpResponse
from rest_framework.views import APIView
from rest_framework.decorators import api_view
from django.http import JsonResponse
import json
import re
from decimal import Decimal

from .models import *
from inventario.models import Llanta
from venta.views import FormatocotizacionHTMLaPDF
from heyoo import WhatsApp

def crear_cotizacion(request, comunicacion):
    cliente = comunicacion.number

    cadena = traeJson(comunicacion, 4)
    clave_seleccionada = cadena['seleccion']
    contenido_seleccionado = cadena['opciones'].get(clave_seleccionada, None)

    # Definir patrones de expresiones regulares para extraer Desc y Clave
    patron_clave = r'\*Clave:\* (.+?)\n'
    patron_desc = r'\*Desc:\* (.+?)\n'

    # Buscar coincidencias usando expresiones regulares
    match_clave = re.search(patron_clave, contenido_seleccionado)
    match_desc = re.search(patron_desc, contenido_seleccionado)

    # Obtener los valores de Desc y Clave
    producto_clave = match_clave.group(1) if match_clave else None
    descripcion = match_desc.group(1) if match_desc else None

    existencias = int(existencia(comunicacion))
    solicita = opcionSeleccionada(comunicacion, 5)
    precio = precio_llanta(comunicacion)

    total = Decimal(solicita) * Decimal(precio)

    datos = {
        'cliente' : cliente,
        'producto_clave' : producto_clave,
        'descripcion' : descripcion,
        'existencia' : existencias,
        'solicita' : solicita,
        'precio' : precio,
        'total': total
    }

    # Crear instancia de la clase FormatoEntregaRemisionHTML
    remision_pdf = FormatocotizacionHTMLaPDF()

    pdf_response = remision_pdf.generar_remision_pdf(datos)

    return pdf_response

def registra_asesor(comunicacion):
    datos = {}

    return datos

# api_view(['POST','GET','PULL','PUT','PATCH','DELETE'])
@api_view(['POST','GET'])
def mensaje_whatsapps(request):
    # Guardado de la información que llega tanto el meodo como la información
    bitacora = Bitacora(descripcion = "Entra")
    bitacora.save()

#    if request.method == 'GET':
#        verify_token = request.GET.get('hub.verify_token', None)
#        hub_challenge = request.GET.get('hub.challenge', '')
#        if verify_token == 'HolaKike':
#            return HttpResponse(hub_challenge)
#        else:
#            return HttpResponse('Error de autenticación')

    bitacora = Bitacora(descripcion = "Entra datos")
    bitacora.save()

    datos=request.data


    #    numero = datos['entry'][0]['changes'][0]['value']['messages'][0]['from']    
    #    mensaje = datos['entry'][0]['changes'][0]['value']['messages'][0]['text']['body']

    numero = '525532171764'
    mensaje = 'Eso es todo'

    if numero:
        opcion_seleccionada = mensaje
        # Busca comunicacion
        comunicacion = MensajePicky.objects.filter(number=numero,estatus_mensaje=1).last()
        message = ""
        respuesta = ""
        if comunicacion:
            # quitar espacion en la cadena del mensaje
            opcion_sel = opcion_seleccionada.upper().replace(" ", "")
            nivel = comunicacion.nivel
            pk = comunicacion.id
            if buscaOpcion(comunicacion, opcion_sel):
                print(nivel)
                if opcion_sel == 'R':
                    # Envia menu anteriror
                    sig_comunicacion = MensajePicky.objects.filter(id=pk).update(nivel=nivel-1)
                    menu_json = traeJson(comunicacion, nivel-1)
                    message = creaMenu(json.dumps(menu_json))
                elif opcion_sel == 'X':
                    sig_comunicacion = MensajePicky.objects.filter(id=pk).update(estatus_mensaje=0)
                    message = "Gracias por su preferencia, lo esperamos muy pronto \n\n"
                elif opcion_sel == 'W':
                    menu_json = traeJson(comunicacion, nivel)
                    menu_json['seleccion'] = opcion_sel

                    crear_cotizacion(comunicacion)
                    envia_cotizacion(comunicacion,'W')

                    upd_comunicacion = MensajePicky.objects.filter(id=pk).update(opcion7=menu_json, estatus_mensaje=0)
                    message = "Cotización enviada \n\n"
                elif opcion_sel == 'A':
                    menu_json = traeJson(comunicacion, nivel)
                    menu_json['seleccion'] = opcion_sel

                    registra_asesor(comunicacion)

                    upd_comunicacion = MensajePicky.objects.filter(id=pk).update(opcion7=menu_json, estatus_mensaje=0)
                    message = "El asesor se comunicará lo antes posible \n\n"
                elif nivel == 7:
                    menu_json = traeJson(comunicacion, nivel)
                    menu_json['seleccion'] = opcion_sel

                    correo_cliente = opcion_sel

                    cotizacionPDF = crear_cotizacion(comunicacion)
                    envia_correo = FormatocotizacionHTMLaPDF()

                    pdf_response = envia_correo.envia_correo(cotizacionPDF, correo_cliente)

                    upd_comunicacion = MensajePicky.objects.filter(id=pk).update(opcion7=menu_json, estatus_mensaje=0)
                    message = "Cotización enviada al correo \n\n"

                else:
                    menu_json = traeJson(comunicacion, nivel)
                    menu_json['seleccion'] = opcion_sel
                    menu_json1 = generaJson(comunicacion, nivel + 1)
                    if nivel == 1:
                        upd_comunicacion = MensajePicky.objects.filter(id=pk).update(opcion1=menu_json, opcion2=menu_json1, nivel=nivel+1)
                    elif nivel == 2:
                        upd_comunicacion = MensajePicky.objects.filter(id=pk).update(opcion2=menu_json, opcion3=menu_json1, nivel=nivel+1)
                    elif nivel == 3:
                        upd_comunicacion = MensajePicky.objects.filter(id=pk).update(opcion3=menu_json, opcion4=menu_json1, nivel=nivel+1)
                    elif nivel == 4:
                        upd_comunicacion = MensajePicky.objects.filter(id=pk).update(opcion4=menu_json, opcion5=menu_json1, nivel=nivel+1)
                    elif nivel == 5:
                        upd_comunicacion = MensajePicky.objects.filter(id=pk).update(opcion5=menu_json, opcion6=menu_json1, nivel=nivel+1)
                    elif nivel == 6:
                        upd_comunicacion = MensajePicky.objects.filter(id=pk).update(opcion6=menu_json, opcion7=menu_json1, nivel=nivel+1)
                    elif nivel == 7:
                        upd_comunicacion = MensajePicky.objects.filter(id=pk).update(opcion7=menu_json, opcion8=menu_json1, nivel=nivel+1)
                    elif nivel == 8:
                        upd_comunicacion = MensajePicky.objects.filter(id=pk).update(opcion8=menu_json, opcion9=menu_json1, nivel=nivel+1)
                    message = creaMenu(json.dumps(menu_json1))
            else:
                # Envia nuevamente el mismo menu
                menu_json = traeJson(comunicacion, nivel)
                message = creaMenu(json.dumps(menu_json))
        else:
            #  Crea el menu primer nivel
            menu_json = generaJson(None, 1)
            message = creaMenu(json.dumps(menu_json))
            
            # Guarda la peticion la primera vez con su primer menu
            comunicacion = MensajePicky(
                number = numero,
                message_in = mensaje,
                message_in_raw = mensaje,
                nivel=1,
                opcion1 = menu_json,
            )
            comunicacion.save()
        # Se envia repuesta 
        # respuesta = {"number":numero,"application":application,"message":message,"type":tipo, "message-out":message,"delay":"0"}
        bitacora = Bitacora(descripcion = 'Arma mensaje')
        bitacora.save()
        respuesta = {"number":numero,"message":message, "message-out":message,"delay":"0"}
        bitacora = Bitacora(descripcion = 'respuesta por enviar')
        bitacora.save()
        envia_respuesta(request, respuesta)
        bitacora = Bitacora(descripcion = 'Termina OK')
        bitacora.save()
        # return Response(respuesta)
        response_data = {"status": "success"}
        return JsonResponse(response_data, status=200)
    else:
        # Se envia el mensaje de error, no envian nada
        bitacora = Bitacora("Faltan datos")
        bitacora.save()
        # return Response(respuesta)
        response_data = {"status": "cancel"}
        return JsonResponse(response_data, status=400)

#    else:
#        # Se envia el mensaje de error, no envian nada
#        respuesta = mensajeError("Sin número")
#        return Response(respuesta)
                
def envia_respuesta(request, respuesta):
    bitacora = Bitacora(descripcion = 'Empieza rutina')
    bitacora.save()
    token = 'EAADwQCYJF8gBO14maxnqEZAfZB8aIOqZCG3G0kELXQtK2cTq7zPjGCfyYSXBulRoY1Uzwg8iqKXCu24g2vfgqZAMd3dn393YDVbT5wbqqcBOkXKLg5fAbi5bQBeJxK8nYk0zIfNP2K7exDfHAjWqpTZAfFmj68FdZBgpZBpkZAoRq8sZAiFnLtvLxqTQEzft7H0JajF5zED0lIzzqcMJqIpkDc6QynhbuqRBiXLoZD'
    bitacora = Bitacora(descripcion = 'Token')
    bitacora.save()
    idTelefonoWhatsapp = '247680495088544'
    bitacora = Bitacora(descripcion = 'idtelefono')
    bitacora.save()
    numeroTelefonoEnviarMensaje = respuesta.get("number", None)
    bitacora = Bitacora(descripcion = 'nuemro a enviar ' + numeroTelefonoEnviarMensaje)
    bitacora.save()
    mensaje = respuesta.get("message", None)
 #   bitacora = Bitacora(descripcion = 'mensaje ' + mensaje)
#    bitacora.save()
    urlLogo = 'core/img/Logo IAG.png'
    bitacora = Bitacora(descripcion = 'Logo' )
    bitacora.save()
    objetoMensaje = WhatsApp(token, phone_number_id=idTelefonoWhatsapp)
#    objetoMensaje = Whatsapp
    bitacora = Bitacora(descripcion = 'objeto')
    bitacora.save()
    objetoMensaje.send_message(mensaje, numeroTelefonoEnviarMensaje)
    bitacora = Bitacora(descripcion = 'envia mensaje')
    bitacora.save()
#    objetoMensaje.send_image(image=urlLogo,recipient_id=numeroTelefonoEnviarMensaje)
    bitacora = Bitacora(descripcion = 'Envia imagen')
    bitacora.save()
    return HttpResponse('Mensaje enviado exitosamente')

def generaJson(comunicacion, nivel):
    opciones = {}
    titulo = ""
    if nivel == 1:
        titulo = "Hola! 👋 Bienvenido al sistema de cotización *Automatizada* de LlantaShop.com 🤖 \n" + \
        "Comencemos, \n" + \
        "➡️ escribe el Ancho de llanta que buscas, son los primeros 3 digitos de tu medida."
        ancho_distinct = Llanta.objects.filter(alto__gt=0, rin__gt=0).values_list('ancho', flat=True).distinct().order_by('ancho')
        registro = 0
        if ancho_distinct:
            for ancho in ancho_distinct:
                registro += 1
                opciones[registro] = ancho
        opciones['X'] = 'Terminar'
    elif nivel == 2:
        ancho = opcionSeleccionadaT(comunicacion, 1)
        anchoN = opcionSeleccionada(comunicacion, 1)
        titulo = "Los altos disponibles para el ancho '" + ancho + "' son:\n\n"
        alto_distinct = Llanta.objects.filter(ancho=ancho, rin__gt=0).values_list('alto', flat=True).distinct().order_by('alto')
        registro = 0
        if alto_distinct:
            for alto in alto_distinct:
                registro += 1
                opciones[registro] = alto
        opciones['R'] = 'Regresar'
        opciones['X'] = 'Terminar'
    elif nivel == 3:
        ancho = opcionSeleccionadaT(comunicacion, 1)
        anchoN = opcionSeleccionada(comunicacion, 1)
        alto = opcionSeleccionadaT(comunicacion, 2)
        altoN = opcionSeleccionada(comunicacion, 2)
        titulo = "Los Diámetros de Rin disponibles para el ancho '" + ancho +"' con alto '" + alto + "' son:\n\n"
        rin_distinct = Llanta.objects.filter(ancho=ancho, alto=alto).values_list('rin', flat=True).distinct().order_by('rin')
        registro = 0
        if rin_distinct:
            for rin in rin_distinct:
                registro += 1
                opciones[registro] = rin
        opciones['R'] = 'Regresar'
        opciones['X'] = 'Terminar'
    elif nivel == 4:
        ancho = opcionSeleccionadaT(comunicacion, 1)
        anchoN = opcionSeleccionada(comunicacion, 1)
        alto = opcionSeleccionadaT(comunicacion, 2)
        altoN = opcionSeleccionada(comunicacion, 2)
        rin = opcionSeleccionadaT(comunicacion, 3)
        rinN = opcionSeleccionada(comunicacion, 3)
        titulo = '📶 Estas son las Marcas y Modelos que tenemos disponibles para entrega inmediata, escoge el que mas te guste y se ajuste a tu presupuesto!\n\n'
        llantas_seleccionadas = Llanta.objects.filter(ancho=ancho, alto=alto, rin=rin)
        registro = 0
        if llantas_seleccionadas:
            for llanta in llantas_seleccionadas:
                registro += 1
                opciones[registro] = "*Clave:*  {}\n*Desc:*  {}\n*Exist:* {}\n*Precio contado: {}*".format(
                    llanta.producto_clave,
                    llanta.descripcion,
                    llanta.existencia,
                    "${:,.2f}".format(llanta.precio)
                )
        opciones['R'] = 'Regresar'
        opciones['X'] = 'Terminar'
    elif nivel == 5:
        ancho = opcionSeleccionadaT(comunicacion, 1)
        anchoN = opcionSeleccionada(comunicacion, 1)
        alto = opcionSeleccionadaT(comunicacion, 2)
        altoN = opcionSeleccionada(comunicacion, 2)
        rin = opcionSeleccionadaT(comunicacion, 3)
        rinN = opcionSeleccionada(comunicacion, 3)
        marca = opcionSeleccionadaT(comunicacion, 4)
        marcaN = opcionSeleccionada(comunicacion, 4)
        titulo = '📶 ¿Cuantas llantas necesitas?\n\n'
        opciones['R'] = 'Regresar'
        opciones['X'] = 'Terminar'
    elif nivel == 6:
        ancho = opcionSeleccionadaT(comunicacion, 1)
        anchoN = opcionSeleccionada(comunicacion, 1)
        alto = opcionSeleccionadaT(comunicacion, 2)
        altoN = opcionSeleccionada(comunicacion, 2)
        rin = opcionSeleccionadaT(comunicacion, 3)
        rinN = opcionSeleccionada(comunicacion, 3)
        marca = opcionSeleccionadaT(comunicacion, 4)
        marcaN = opcionSeleccionada(comunicacion, 4)
        cant = opcionSeleccionada(comunicacion, 5)
        cantN = opcionSeleccionada(comunicacion, 5)
        titulo = '📶 ¿Como quieres que te envie la cotización?\n\n'
        opciones['W'] = 'Whatsapp'
        opciones['C'] = 'Correo'
        opciones['A'] = 'o ¿Quieres que se comunique un asesor contigo?'
        opciones['R'] = 'Regresar'
        opciones['X'] = 'Terminar'
    elif nivel == 7:
        ancho = opcionSeleccionadaT(comunicacion, 1)
        anchoN = opcionSeleccionada(comunicacion, 1)
        alto = opcionSeleccionadaT(comunicacion, 2)
        altoN = opcionSeleccionada(comunicacion, 2)
        rin = opcionSeleccionadaT(comunicacion, 3)
        rinN = opcionSeleccionada(comunicacion, 3)
        marca = opcionSeleccionadaT(comunicacion, 4)
        marcaN = opcionSeleccionada(comunicacion, 4)
        cant = opcionSeleccionada(comunicacion, 5)
        cantN = opcionSeleccionada(comunicacion, 5)
        enviocot = opcionSeleccionadaT(comunicacion, 6)
        enviocotN = opcionSeleccionada(comunicacion, 6)
        titulo = '📶 Dame tu correo ...\n\n'
        opciones['R'] = 'Regresar'
        opciones['X'] = 'Terminar'
    data = {'titulo': titulo, 'seleccion':0, 'opciones': opciones}
    return data

def buscaOpcion(comunicacion, opcion_sel):
    nivel = comunicacion.nivel
    menu_json = traeJson(comunicacion, nivel)
    return existeOpcion(menu_json, opcion_sel)

def traeJson(comunicacion, opcion):
    if opcion == 1:
        menu_json = comunicacion.opcion1
    elif opcion == 2:
        menu_json = comunicacion.opcion2
    elif opcion == 3:
        menu_json = comunicacion.opcion3
    elif opcion == 4:
        menu_json = comunicacion.opcion4
    elif opcion == 5:
        menu_json = comunicacion.opcion5
    elif opcion == 6:
        menu_json = comunicacion.opcion6
    else:
        menu_json = comunicacion.opcion7
    return menu_json

def existeOpcion(menu_json, opcion_sel):
    encontro = False
    cadena = menu_json['titulo']
    subcadena1 = 'Dame tu correo'
    subcadena2 = 'Cuantas llantas necesitas'
    if subcadena2 in cadena:
        if opcion_sel in['X','R']:
            encontro = True
        elif opcion_sel.isdigit():
            if int(opcion_sel) > 0:
                encontro = True
    elif subcadena1 in cadena:
        if validar_correo(opcion_sel) or opcion_sel in['X','R']:
            encontro = True
    else:
        for opcion in menu_json['opciones']:
            if opcion == opcion_sel:
                encontro = True
                break
    return encontro
                
def opcionSeleccionada(comunicacion, opcion):
    opcion_sel = traeJson(comunicacion, opcion)
    seleccion = opcion_sel['seleccion']
    return seleccion

def opcionSeleccionadaT(comunicacion, opcion):
    opcion_sel = traeJson(comunicacion, opcion)
    seleccion = opcion_sel['seleccion']
    return opcion_sel['opciones'][seleccion]

def existencia(comunicacion):
    opcion_sel = traeJson(comunicacion, 4)
    seleccion = opcion_sel['seleccion']
    exist_valor = re.search(r'\*Exist:\*\s*(\d+)', opcion_sel['opciones'][seleccion])
    existencia_llanta = exist_valor.group(1)
    return existencia_llanta

def precio_llanta(comunicacion):
    opcion_sel = traeJson(comunicacion, 4)
    seleccion = opcion_sel['seleccion']
    precio_valor = re.search(r'\*Precio contado:\s*\$(\d+\.\d+)', opcion_sel['opciones'][seleccion])
    precio = precio_valor.group(1)
    return precio

def correo_cliente(comunicacion):
    opcion_sel = traeJson(comunicacion, 7)
    correo = opcion_sel['seleccion']
    return correo

def creaMenu(objeto):
    json_data = json.loads(objeto)
    mensaje = json_data['titulo']
    if json_data['opciones']:
        opciones = json_data['opciones']
        for opcion in opciones:
            mensaje += opcion + " - " + opciones[opcion] + "\n"
    return mensaje

def mensajeError(numeroTelefono):
    mensaje = 'Faltan datos'
    respuesta = {'Error':mensaje}
    bitacora = Bitacora(descripcion = "Celular:" + 'RRR' + "/" + mensaje)
    bitacora.save()
    return respuesta

def validar_correo(correo):
    # Patrón de expresión regular para validar un correo electrónico
    patron_correo = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'

    # Aplicar el patrón y verificar si coincide
    if re.match(patron_correo, correo):
        return True
    else:
        return False

