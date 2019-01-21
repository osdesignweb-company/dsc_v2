# -*- coding: utf-8 -*-
from __future__ import unicode_literals


from django.contrib import admin
from dashboard.models import Paises, Departamentos, Municipios

admin.site.register(Paises)
admin.site.register(Departamentos)
admin.site.register(Municipios)