from django.shortcuts import render
from django.views import View
import pandas as pd
from django.db import IntegrityError, transaction

from .forms import *
from core.models import Llanta

# Create your views here.

class Importa_archivo(View):
    def get(self, request):
        form = ExcelForm()
        return render(request, 'importa/carga_excel.html', {'form': form})

    def post(self, request):
        reg_ok = 0
        reg_nok = 0
        reg_total = 0
        context = {}
        mensajes = ''
        otro = 'Otro'
        form = ExcelForm(request.POST, request.FILES)
        if form.is_valid():
            archivo = request.FILES['archivo_excel']
            df = pd.read_excel(archivo, sheet_name=None)  # Leer todas las hojas
            for hoja, datos in df.items():
                if hoja == 'llantas':
                    for index, row in datos.iterrows():
                        if index >= 0:
                            producto_clave=row[1]
                            descripcion=row[2]
                            ancho=row[3]
                            alto=row[4]
                            rin=row[5]
                            existencia=row[6]
                            costo_promedio_pesos=row[7]
                            reg_total += 1
                            try:
                                llanta, created = Llanta.objects.get_or_create(
                                    producto_clave=producto_clave,
                                    descripcion=descripcion,
                                    ancho=ancho,
                                    alto=alto,
                                    rin=rin,
                                    existencia=existencia,
                                    costo_promedio_pesos=costo_promedio_pesos,
                                )
                                if created:
                                    # El objeto se creó porque no existía previamente
                                    reg_ok += 1
                                    llanta.save()
                                else:
                                    # El objeto ya existía con la misma clave, puedes manejar la duplicidad aquí
                                    mensajes += 'Registro duplicado por clave (' + row[1] + ') o descripción (' + row[2] + ')' + \
                                        ' en el la hoja Materiales renglón ' + str(index + 2) + ' \n '
                                    reg_nok += 1
                                    pass
                            except IntegrityError:
                                # Aquí puedes manejar la excepción si ocurre un error de unicidad (clave duplicada)
                                mensajes += 'Registro duplicado por clave (' + row[1] + ') o descripción (' + row[2] + ')' + \
                                    ' en el la hoja Materiales renglón ' + str(index + 2) + ' \n '
                                reg_nok += 1
                                pass
            context['llantas'] = Llanta.objects.all()
            context['reg_ok'] = reg_ok
            context['reg_nok'] = reg_nok
            context['reg_total'] = reg_total
            context['mensajes'] = mensajes
            return render(request, 'importa/exito.html', context=context)
        else:
            return render(request, 'importa/cargar_excel.html', {'form': form})