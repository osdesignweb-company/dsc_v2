# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render, redirect
from public.forms import LoginForm
from usuarios.models import Usuario as User
from django.contrib.auth import get_user_model
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse

#Index View
def index(request):
    #return 
    return render(request,'public/index.html')

#Login view
def login_view(request):
    form = LoginForm()
    if request.method == 'POST':
        if form.is_valid:
            id_persona = request.POST.get('id_persona')
            password = request.POST.get('password')
            user = authenticate(request, id_persona=id_persona, password=password)
            if user:
                login(request,user)
                return redirect('dashboard:dashboard')
            else:
                return render(request, 'public/login.html',{'error': 'Usuarios y/o password erroneos','form':form})
    
    return render(request, 'public/login.html',{'form':form})
    #return HttpResponse("OK")

#Logout view
@login_required
def logout_view(request):
	logout(request)
	return redirect('public:login')