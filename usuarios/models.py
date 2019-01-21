# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin

from dashboard.models import Paises

class PersonalizarBaseUserManager(BaseUserManager):
    def create_user(self, id_persona, password):
        user = self.model(id_persona=id_persona)        
        user.set_password(password)
        user.rol = 2
        user.save(using=self._db)
        return user
    
    def create_staffuser(self, id_persona, password):
        user = self.create_user(id_persona, password)
        user.is_staff = True
        user.is_admin = False
        user.rol = 1
        user.save(using=self._db)
        return user
    
    def create_superuser(self, id_persona, password):
        user = self.create_user(id_persona, password)
        user.is_superuser = True
        user.is_staff = True
        user.is_admin = True
        user.rol = 1
        user.save(using=self._db)
        return user
    
    # def nombre_completo(self,nombre,primer_apellido):
    #     return '{} {}'.format(self.nombre, self.primer_apellido)

class Usuario(AbstractBaseUser, PermissionsMixin):
    id_persona = models.CharField(max_length=10,unique=True,primary_key=True)
    nombre = models.CharField(max_length=100, blank=True)
    primer_apellido = models.CharField(max_length=50, blank=True)
    segundo_apellido = models.CharField(max_length=50, blank=True)

    tipo_documento_choices = (
        (0,'Cédula de ciudadanía'),
        (1,'Cédula Extranjera'),
        (2, 'Pasaporte'),
        (3, 'Tarjeta de identidad'),
    ) 

    rol_choices = (
        (1,'Admin'),
        (2,'User'),
    )

    sexo_choices = (
        (1, 'Femenino'),
        (2, 'Masculino')
    )

    tipo_documento = models.IntegerField(choices=tipo_documento_choices, default=0)
    rol = models.IntegerField(choices=rol_choices, default=2)
    sexo = models.IntegerField(choices=sexo_choices,blank=True, null=True)
    correo = models.EmailField(max_length=100,blank=True)
    celular = models.CharField(max_length=13,blank=True)
    telefono = models.CharField(max_length=10,blank=True)
    pais_nacimiento = models.ForeignKey(Paises,models.DO_NOTHING, blank=True, null=True)
    imagen = models.ImageField(upload_to='usuarios/imagen_perfil/', blank=True, null=True) 
    fecha_nacimiento = models.DateField(blank=True, null=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False) # a admin user; non super-user
    is_admin = models.BooleanField(default=False) # a superuser
    creado = models.DateTimeField(auto_now_add=True)
    modificado = models.DateTimeField(auto_now=True)

    USERNAME_FIELD = 'id_persona'

    objects = PersonalizarBaseUserManager()

    def get_full_name(self):
        return '{} {}'.format(self.nombre, self.primer_apellido)
    
    def get_short_name(self):
        return self.nombre
    
    def __str__(self): 
        return self.id_persona

    def has_perm(self, perm, obj=None):
        "Does the user have a specific permission?"
        return True
    
    def has_module_perms(self, app_label):
        "Does the user have permissions to view the app `app_label`?"
        return True