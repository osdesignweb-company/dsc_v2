# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.shortcuts import render
from .forms import MunicipioForm, EdadesForm, PersonaSDForm, PersonaCDForm, DescripcionForm
from .models import DescripcionFormulario, MunicipioAfectado, Edades, PersonasSinDiscapacidad, PersonasConDiscapacidad
from dashboard.models import Municipios, Departamentos
from django.contrib.auth.decorators import login_required

from django.contrib.auth import get_user_model

import xlsxwriter, openpyxl, os


from django.http import HttpResponse

@login_required
def formulario_view(request):
    print("HOla")
    fullname = request.user.get_full_name()

    municipio_form = MunicipioForm()
    edad_form = EdadesForm()
    personassd_form = PersonaSDForm()
    personascd_form = PersonaCDForm()
    descripcion_form = DescripcionForm(
        {
            "correo" : request.user.correo,
            "cedula" : request.user.id_persona,
            "nombre_operador" : request.user.get_full_name(),
            "persona_diligencia" : request.user,
            "telefono" : request.user.telefono
        }
    )

    if request.method == "POST":

        maestro_form = None
        if request.POST["add-value"] == "true":
            maestro_form = DescripcionFormulario.objects.all()
            maestro_form = maestro_form.last()
        else:
            descripcion_dict = {
                'fecha_presentacion': request.POST["fecha_presentacion"],
                'mes_reportado': request.POST["mes_reportado"],
                'departamento': Departamentos.objects.get(
                    id_departamento = request.POST["departamento"]
                ),
                'municipio_form': Municipios.objects.get(
                    id_municipio = request.POST["municipio_form"]
                ),
                'nombre_proyecto': request.POST["nombre_proyecto"],
                'nombre_operador': request.POST["nombre_operador"],
                'cargo': request.POST["cargo"],
                'cedula' : request.user,
                'num_contrato': request.POST["num_contrato"],
                'fecha_inicio': request.POST["fecha_inicio"],
                'fecha_fin' : request.POST["fecha_fin"],
                'persona_diligencia' : request.POST["persona_diligencia"],
                'correo' : request.POST["correo"],
                'telefono' : request.POST["telefono"]
            }
            maestro_form = DescripcionFormulario(**descripcion_dict)

        maestro_form.save()
        
        municipio_dict = {
            "municipio_fk" : Municipios.objects.get(
                id_municipio = request.POST["municipio_fk"]
            ),
            "poblacion" : request.POST["poblacion"],
            "descripcion" : maestro_form
        }
        municipio_afectado = MunicipioAfectado(**municipio_dict)
        municipio_afectado.save()

        edades_dict = {
            "municipio" : municipio_afectado,
            "de_0_a_6" : request.POST["de_0_a_6"], 
            "de_7_a_11" : request.POST["de_7_a_11" ], 
            "de_12_a_14" : request.POST["de_12_a_14"],
            "de_15_a_17" : request.POST["de_15_a_17"],
            "de_18_a_25" : request.POST["de_18_a_25"],
            "de_26_a_60" : request.POST["de_26_a_60"],
            "mas_de_60" : request.POST["mas_de_60"]
        }

        #Guarda con el kwargs del diccionario
        edad = Edades(
            **edades_dict
        )
        #elimina las llaves que no necesita para el calculo
        edades_dict.pop("municipio")
        acum = 0
        for k,v in edades_dict.items():
            acum += int(v)
        #calcula y guarda el total
        edad.total_edad = acum
        edad.save()

        personas_sd_dict = {
            "municipio" : municipio_afectado,
            "cant_indigenas_m" : request.POST["cant_indigenas_m"],
            "cant_indigenas_f" : request.POST["cant_indigenas_f"],
            "cant_afro_m" : request.POST["cant_afro_m"],
            "cant_afro_f" : request.POST["cant_afro_f"],
            "cant_raizal_m" : request.POST["cant_raizal_m"],
            "cant_raizal_f" : request.POST["cant_raizal_f"],
            "cant_palenque_m" : request.POST["cant_palenque_m"],
            "cant_palenque_f" : request.POST["cant_palenque_f"],
            "cant_campesino_m" : request.POST["cant_campesino_m"],
            "cant_campesino_f" : request.POST["cant_campesino_f"],
            "cant_romm_m" : request.POST["cant_romm_m"],
            "cant_romm_f" : request.POST["cant_romm_f"],
            "cant_lgbti" : request.POST["cant_lgbti"],
            "cant_singrupo_m" : request.POST["cant_singrupo_m"],
            "cant_singrupo_f" : request.POST["cant_singrupo_f"]
        }

        personas_sd = PersonasSinDiscapacidad(
            **personas_sd_dict
        )
        personas_sd_dict.pop("municipio")

        acum_sd_m = 0
        acum_sd_f = 0
        for k,v in personas_sd_dict.items():
            #calcula los totales segun hombres y mujeres
            if k[-1] == 'm':
                acum_sd_m += int(v)
            elif k[-1] == 'f':
                acum_sd_f += int(v)
        
        #Total de las poblaciones
        total_psd = acum_sd_f + acum_sd_m + int(request.POST["cant_lgbti"])
        #Asignando los totales segun sexo
        personas_sd.total_m = acum_sd_m
        personas_sd.total_f = acum_sd_f
        personas_sd.total_poblacion = total_psd
        personas_sd.save()

        personas_cd_dict = {
            "municipio" : municipio_afectado,
            "cant_fisica_m" : request.POST["cant_fisica_m"],
            "cant_fisica_f" : request.POST["cant_fisica_f"],
            "cant_sensorial_m" : request.POST["cant_sensorial_m"],
            "cant_sensorial_f" : request.POST["cant_sensorial_f"],
            "cant_intelectual_m" : request.POST["cant_intelectual_m"],
            "cant_intelectual_f" : request.POST["cant_intelectual_f"]
        }

        personas_cd = PersonasConDiscapacidad(
            **personas_cd_dict
        )
        personas_cd_dict.pop("municipio")

        acum_cd_f = 0
        acum_cd_m = 0
        for k,v in personas_cd_dict.items():
            if k[-1] == 'm':
                acum_cd_m += int(v)
            elif k[-1] == 'f':
                acum_cd_f += int(v)
        
        total_pcd = acum_cd_f + acum_cd_m
        #Asignando los totales segun sexo
        personas_cd.total_m = acum_cd_m
        personas_cd.total_f = acum_cd_f
        personas_cd.total_poblacion = total_pcd
        personas_cd.save()
        
    else:
        pass
        

    return render(
        request, 
        'formularios/formulario_registro_usuarios.html',
        {
            "municipio_form" : municipio_form,
            "edad_form" : edad_form,
            "personas_sd_form" : personassd_form,
            "personas_cd_form" : personascd_form,
            "descripcion_form" : descripcion_form,
            "fullname":fullname
        }
        
    )

@login_required
def export_users_excel(request, id_maestro):
    
    maestro = DescripcionFormulario.objects.get(pk=id_maestro)
    file_path = "/opt/dscproject/media/reporte.xlsx"
    book = openpyxl.load_workbook(file_path)
    sheet = book.active

    #asignando los valores segun las celdas correspondientes

    sheet['J6'] = str(maestro.fecha_presentacion)
    sheet['V6'] = str(maestro.mes_reportado)
    sheet['AG6'] = str(maestro.departamento.departamento)

    sheet['J7'] = str(maestro.municipio_form.municipio)
    sheet['V7'] = str(maestro.nombre_proyecto)
    sheet['AG7'] = str(maestro.nombre_operador)

    sheet['J8'] = str(maestro.persona_diligencia)
    sheet['V8'] = str(maestro.cargo)
    sheet['AG8'] = str(maestro.cedula)

    sheet['J9'] = str(maestro.num_contrato)
    sheet['V9'] = str(maestro.fecha_inicio)
    sheet['AG9'] = str(maestro.fecha_fin)

    sheet['J10'] = str(maestro.telefono)
    sheet['V10'] = str(maestro.correo)

    list_municipios = MunicipioAfectado.objects.filter(descripcion=maestro.id)
    print(list_municipios)

    i = 15
    for item in list_municipios:

        sheet['A'+str(i)] = str(item.municipio_fk.municipio)
        

        list_edades = Edades.objects.filter(municipio=item)
        j = i
        for edad in list_edades:
            sheet['C'+str(j)] = str(edad.de_0_a_6)
            sheet['D'+str(j)] = str(edad.de_7_a_11)
            sheet['E'+str(j)] = str(edad.de_12_a_14)
            sheet['F'+str(j)] = str(edad.de_15_a_17)
            sheet['G'+str(j)] = str(edad.de_18_a_25)
            sheet['H'+str(j)] = str(edad.de_26_a_60)
            sheet['I'+str(j)] = str(edad.mas_de_60)
            j += 1 
        
        list_sin_discapacidad = PersonasSinDiscapacidad.objects.filter(municipio=item)
        k = i
        for persona in list_sin_discapacidad:
            sheet['L'+str(k)] = str(persona.cant_indigenas_m)
            sheet['M'+str(k)] = str(persona.cant_indigenas_f)

            sheet['N'+str(k)] = str(persona.cant_afro_m)
            sheet['O'+str(k)] = str(persona.cant_afro_f)

            sheet['P'+str(k)] = str(persona.cant_raizal_m)
            sheet['Q'+str(k)] = str(persona.cant_raizal_f)

            sheet['R'+str(k)] = str(persona.cant_palenque_m)
            sheet['S'+str(k)] = str(persona.cant_palenque_f)

            sheet['T'+str(k)] = str(persona.cant_campesino_m)
            sheet['U'+str(k)] = str(persona.cant_campesino_f)

            sheet['V'+str(k)] = str(persona.cant_romm_m)
            sheet['W'+str(k)] = str(persona.cant_romm_f)

            sheet['X'+str(k)] = str(persona.cant_lgbti)

            sheet['Y'+str(k)] = str(persona.cant_singrupo_m)
            sheet['Z'+str(k)] = str(persona.cant_singrupo_f)
            k += 1

        list_con_discapacidad = PersonasConDiscapacidad.objects.filter(municipio=item)
        m = i
        for persona in list_con_discapacidad:
            sheet['AD'+str(m)] = str(persona.cant_fisica_m)
            sheet['AE'+str(m)] = str(persona.cant_fisica_f)

            sheet['AF'+str(m)] = str(persona.cant_sensorial_m)
            sheet['AG'+str(m)] = str(persona.cant_sensorial_f)

            sheet['AH'+str(m)] = str(persona.cant_intelectual_m)
            sheet['AI'+str(m)] = str(persona.cant_intelectual_f)
            m += 1
        
        i += 2


    book.save('reporte'+str(maestro.id)+'.xlsx')
   



    file_path_download = 'reporte'+str(maestro.id)+'.xlsx'
    if os.path.exists(file_path_download):
        with open(file_path_download, 'rb') as fh:
            response = HttpResponse(fh.read(), content_type="application/vnd.ms-excel")
            response['Content-Disposition'] = 'inline; filename=' + os.path.basename(file_path_download)
            return response
    raise Http404



