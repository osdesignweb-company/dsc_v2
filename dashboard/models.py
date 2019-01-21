# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models

class Paises(models.Model):
    id_pais = models.CharField(primary_key=True,max_length=3)
    pais = models.CharField(max_length=70)

    class Meta:
        managed = True
        db_table = 'paises'
        verbose_name='Pais'
        verbose_name_plural ='Paises'
                
    def __str__(self):
        return self.pais

class Departamentos(models.Model):
    id_departamento = models.CharField(primary_key=True,max_length=2)
    id_pais = models.ForeignKey(Paises,models.DO_NOTHING,db_column='id_pais')
    departamento = models.CharField(max_length=30)

    class Meta:
        managed = True
        db_table = 'departamentos'
        verbose_name='Departamentos'
        verbose_name_plural ='Departamentos'
                
    def __str__(self):
        return self.departamento

class Municipios(models.Model):
    id_municipio = models.CharField(primary_key=True,max_length=5)
    id_departamento = models.ForeignKey(Departamentos,models.DO_NOTHING,db_column='id_departamento')
    municipio = models.CharField(max_length=50)
    flag = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = True
        db_table = 'municipios'
        verbose_name='Municipios'
        verbose_name_plural ='Municipios'
                
    def __str__(self):
        return self.municipio