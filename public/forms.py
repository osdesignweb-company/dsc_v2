# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django import forms
from django.contrib.auth import get_user_model
from django.utils.translation import ugettext_lazy as _
from django.core.validators import MaxValueValidator, MinValueValidator

class LoginForm(forms.ModelForm):
    id_persona = forms.CharField(label='N° Documento',required=True) 
    password = forms.CharField(label='Password',min_length=8,widget=forms.PasswordInput)

    class Meta:
        model =  get_user_model()
        fields = ('id_persona','password',)