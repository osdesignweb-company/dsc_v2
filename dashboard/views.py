# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.conf import settings
from django.contrib import messages
from django.http import HttpResponse
from django.contrib.auth import get_user_model, update_session_auth_hash
# Atributos para que solo ingresen usuarios registrados
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect, render
from django.utils.html import escape
from django.views.generic import ListView, UpdateView

# Forms
from dashboard.forms import UserCreationForm, UserUpdateForm

from formularios.models import DescripcionFormulario

import json
from builtins import super
from django.core.serializers.json import DjangoJSONEncoder
from django.core import serializers


# Dashboard View
@login_required
def DashboardView(request):
	fullname = request.user.get_full_name()
	return render(request,'dashboard/index.html', {'user': request.user,'fullname':fullname})

@login_required
def CrearPersonaView(request):
    fullname = request.user.get_full_name()
    if request.method == 'POST':
        form = UserCreationForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            form = UserCreationForm()
            messages.success(request, 'Usuario creado exitosamente!')
            return render(request,'dashboard/crear_persona.html', {'user': request.user,'fullname':fullname,'form':form})
        else:
            messages.error(request, 'Corrije los siguientes errores')
    else:
        form = UserCreationForm()
    return render(request,'dashboard/crear_persona.html', {'user': request.user,'fullname':fullname,'form':form})

@login_required
def CambiarPasswordView(request):
    fullname = request.user.get_full_name()
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)  # Important!
            messages.success(request, 'Contraseña actualizada exitosamente!')
            return render(request, 'dashboard/cambiar_password.html', {'user': request.user,'fullname':fullname,'form':form})
        else:
            messages.error(request, 'Corrije los siguientes errores')
    else:
        form = PasswordChangeForm(request.user)
    return render(request, 'dashboard/cambiar_password.html', {'user': request.user,'fullname':fullname,'form':form})

class PersonasList(LoginRequiredMixin,ListView):
    model = get_user_model()
    template_name = 'dashboard/personas.html'
    context_object_name = 'users'

    # Filtro superusuarios
    def get_queryset(self):
        return get_user_model().objects.all().filter(is_superuser = False)
    
    def get_context_data(self,**kwargs):
        context = super().get_context_data(**kwargs)
        context['fullname'] = self.request.user.get_full_name()
        return context

@login_required
def PersonaUnicaView(request,id_persona):
    fullname = request.user.get_full_name()
    persona = get_user_model().objects.get(id_persona = id_persona)
    if request.method == 'POST':
	    form = UserUpdateForm(request.POST, request.FILES,instance=persona)
	    if form.is_valid():
	    	form.save()
	    	form = UserUpdateForm(instance=persona)
	    	messages.success(request, 'Usuario actualizado exitosamente!')
	    	return render(request,'dashboard/persona_unica.html', {'user': request.user,'fullname':fullname,'form':form,'persona':persona})
	    else:
	    	messages.error(request, 'Corrije los siguientes errores')
    else:
        form = UserUpdateForm(instance=persona)
        
    return render(request, 'dashboard/persona_unica.html', {'user': request.user,'fullname':fullname,'form':form,'persona':persona})

@login_required
def CambiarPerfilUsuarioView(request):
    fullname = request.user.get_full_name()
    persona = request.user
    if request.method == 'POST':
	    form = UserUpdateForm(request.POST, request.FILES,instance=persona)
	    if form.is_valid():
	    	form.save()
	    	form = UserUpdateForm(instance=persona)
	    	messages.success(request, 'Perfil actualizado exitosamente!')
	    	return render(request,'dashboard/perfil_persona.html', {'user': request.user,'fullname':fullname,'form':form,'persona':persona})
	    else:
	    	messages.error(request, 'Corrije los siguientes errores')
    else:
        form = UserUpdateForm(instance=persona)
        
    return render(request, 'dashboard/perfil_persona.html', {'user': request.user,'fullname':fullname,'form':form,'persona':persona})

@login_required
def BorrarUsuarioView(request,id_persona):
    fullname = request.user.get_full_name()
    user = get_user_model().objects.get(id_persona = id_persona)
    user.delete()
    messages.success(request, "The user is deleted")
    # return HttpResponse('Usuario Borrado')    
    return render(request,'dashboard/index.html', {'user': request.user,'fullname':fullname})

@login_required
def Test(request):
    fullname = request.user.get_full_name()
    # persona = get_user_model().objects.all().filter(is_superuser = False).values_list('nombre', flat=True).distinct()
    # persona = list(get_user_model().objects.all().filter(is_superuser = False).values_list('nombre', flat=True).distinct())

    persona = json.dumps([dict(item) for item in get_user_model().objects.all().filter(is_superuser = False).values('nombre', 'primer_apellido', 'segundo_apellido','id_persona' )])
    # data  = json.loads(persona1)

    return render(request,'dashboard/test.html', {'personas' : persona})

@login_required
def MetricasRegistroUsuariosView(request):
	fullname = request.user.get_full_name()
	lista_formulario_maestro = DescripcionFormulario.objects.all()
	return render(request, 'dashboard/metricas_registro_usuarios.html', {'user': request.user,'fullname':fullname, 'lista':lista_formulario_maestro})

@login_required
def BorrarFormlarioView(request, id_form):
    fullname = request.user.get_full_name()
    form = DescripcionFormulario.objects.get(id = id_form)
    form.delete()
    messages.success(request, "El registro ha sido borrado exitosamente!")
    lista_formulario_maestro = DescripcionFormulario.objects.all()
    # return HttpResponse('Usuario Borrado')    
    return render(request, 'dashboard/metricas_registro_usuarios.html', {'user': request.user,'fullname':fullname, 'lista':lista_formulario_maestro})