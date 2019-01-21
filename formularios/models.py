# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from functools import reduce
from dashboard.models import Municipios, Departamentos
from django.contrib.auth import get_user_model
from django.conf import settings

class DescripcionFormulario(models.Model):
    mes_choices = (
        ('ENERO','ENERO'),
        ('FEBRERO','FEBRERO'),
        ('MARZO','MARZO'),
        ('ABRIL','ABRIL'),
        ('MAYO','MAYO'),
        ('JUNIO','JUNIO'),
        ('JULIO','JULIO'),
        ('AGOSTO','AGOSTO'),
        ('SEPTIEMBRE','SEPTIEMBRE'),
        ('OCTUBRE','OCTUBRE'),
        ('NOVIEMBRE','NOVIEMBRE'),
        ('DICIEMBRE','DICIEMBRE'),
    ) 

    fecha_presentacion = models.DateField(auto_now=False, auto_now_add=False)
    mes_reportado = models.CharField(choices=mes_choices,max_length=20)
    departamento = models.ForeignKey(Departamentos, on_delete=models.CASCADE)
    municipio_form = models.ForeignKey(Municipios, on_delete=models.CASCADE)
    nombre_proyecto = models.CharField(max_length=20)
    nombre_operador = models.CharField(max_length=20)
    cargo = models.CharField(max_length=20)
    cedula = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    num_contrato = models.CharField(max_length=50)
    fecha_inicio = models.DateField(auto_now=False, auto_now_add=False)
    fecha_fin = models.DateField(auto_now=False, auto_now_add=False)
    #persona_diligencia = models.CharField(max_length=20)
    persona_diligencia = models.CharField(max_length=20)
    creado = models.DateTimeField(auto_now_add=True)
    correo = models.CharField(max_length=50, null=True)
    telefono = models.CharField(max_length=20)


class MunicipioAfectado(models.Model):

    poblacion_choices = (
        ('RURAL','RURAL'),
        ('URBANO','URBANO')
    )

    municipio_fk = models.ForeignKey(Municipios, on_delete=models.CASCADE) #aqui va la foranea de municipio
    total = models.IntegerField(default=0)
    poblacion = models.CharField(choices=poblacion_choices,max_length=20)
    descripcion = models.ForeignKey(DescripcionFormulario, on_delete=models.CASCADE)


class Edades(models.Model):    
    municipio = models.ForeignKey(MunicipioAfectado, on_delete=models.CASCADE)
    total_edad = models.IntegerField(default=0)
    de_0_a_6 = models.IntegerField(default=0)
    de_7_a_11 = models.IntegerField(default=0)
    de_12_a_14 = models.IntegerField(default=0)
    de_15_a_17 = models.IntegerField(default=0)
    de_18_a_25 = models.IntegerField(default=0)
    de_26_a_60 = models.IntegerField(default=0)
    mas_de_60 = models.IntegerField(default=0)

class PersonasSinDiscapacidad(models.Model):

    municipio = models.ForeignKey(MunicipioAfectado, on_delete=models.CASCADE)
    cant_indigenas_m = models.IntegerField(default=0)
    cant_indigenas_f = models.IntegerField(default=0)
    cant_afro_m = models.IntegerField(default=0)
    cant_afro_f = models.IntegerField(default=0)
    cant_raizal_m = models.IntegerField(default=0)
    cant_raizal_f = models.IntegerField(default=0)
    cant_palenque_m = models.IntegerField(default=0)
    cant_palenque_f = models.IntegerField(default=0)
    cant_campesino_m = models.IntegerField(default=0)
    cant_campesino_f = models.IntegerField(default=0)
    cant_romm_m = models.IntegerField(default=0)
    cant_romm_f = models.IntegerField(default=0)
    cant_lgbti = models.IntegerField(default=0)
    cant_singrupo_m = models.IntegerField(default=0)
    cant_singrupo_f = models.IntegerField(default=0)
    total_m = models.IntegerField(default=0)
    total_f = models.IntegerField(default=0)
    total_poblacion = models.IntegerField(default=0)

class PersonasConDiscapacidad(models.Model):

    municipio = models.ForeignKey(MunicipioAfectado, on_delete=models.CASCADE)
    cant_fisica_m = models.IntegerField(default=0)
    cant_fisica_f = models.IntegerField(default=0)
    cant_sensorial_m = models.IntegerField(default=0)
    cant_sensorial_f = models.IntegerField(default=0)
    cant_intelectual_m = models.IntegerField(default=0)
    cant_intelectual_f = models.IntegerField(default=0)
    total_m = models.IntegerField(default=0)
    total_f = models.IntegerField(default=0)
    total_poblacion = models.IntegerField(default=0)

