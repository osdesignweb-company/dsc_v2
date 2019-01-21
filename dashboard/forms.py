# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django import forms
from django.contrib.auth import get_user_model

from django.views.generic.edit import UpdateView
from django.urls import reverse

from builtins import super


class UserCreationForm(forms.ModelForm):
    # id_persona = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'N° Documento'}))
    nombre = forms.CharField(required=True)
    primer_apellido = forms.CharField(required=True)
    password1 = forms.CharField(label='Password', min_length=8, widget=forms.PasswordInput)
    password2 = forms.CharField(label='Password confirmation', min_length=8, widget=forms.PasswordInput)

    class Meta:
        model = get_user_model()
        fields = ('id_persona','nombre','primer_apellido','segundo_apellido',
            'tipo_documento','rol','sexo','correo','celular','telefono',
            'pais_nacimiento','imagen','fecha_nacimiento',
        )

    def clean_password2(self):
        # Check that the two password entries match
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Contraseñas no coinciden")
        return password2

    def save(self, commit=True):
        # Save the provided password in hashed format
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user

class UserUpdateForm(forms.ModelForm):
    class Meta:
        model = get_user_model()
        fields = (
            'id_persona','nombre','primer_apellido','segundo_apellido',
            'tipo_documento','rol','sexo','correo','celular','telefono',
            'pais_nacimiento','imagen','fecha_nacimiento',
        )

    def save(self, commit=True):
        user = super().save(commit=False)        
        if commit:
            user.save()
        return user