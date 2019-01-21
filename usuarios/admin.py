# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin
from usuarios.models import Usuario
from django.contrib.auth.admin import UserAdmin
# Register your models here.

class PersonalizadoUserAdmin(UserAdmin):
    fieldsets = ()
    add_fieldsets = (
        (None, {
            'fields': ('id_persona','nombre','primer_apellido','segundo_apellido','password1','password2'),
        }),
    )

    list_display = ('id_persona','nombre','primer_apellido','rol','is_active','is_staff','is_admin')
    search_fields = ('id_persona','nombre')
    ordering = ('id_persona',)

    readonly_fields = ('creado', 'modificado',)

admin.site.register(Usuario, PersonalizadoUserAdmin)