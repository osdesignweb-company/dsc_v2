# -*- coding: utf-8 -*-
# Generated by Django 1.11.18 on 2019-01-20 02:04
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0008_alter_user_username_max_length'),
        ('dashboard', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Usuario',
            fields=[
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('id_persona', models.CharField(max_length=10, primary_key=True, serialize=False, unique=True)),
                ('nombre', models.CharField(blank=True, max_length=100)),
                ('primer_apellido', models.CharField(blank=True, max_length=50)),
                ('segundo_apellido', models.CharField(blank=True, max_length=50)),
                ('tipo_documento', models.IntegerField(choices=[(0, 'C\xe9dula de ciudadan\xeda'), (1, 'C\xe9dula Extranjera'), (2, 'Pasaporte'), (3, 'Tarjeta de identidad')], default=0)),
                ('rol', models.IntegerField(choices=[(1, 'Admin'), (2, 'User')], default=2)),
                ('sexo', models.IntegerField(blank=True, choices=[(1, 'Femenino'), (2, 'Masculino')], null=True)),
                ('correo', models.EmailField(blank=True, max_length=100)),
                ('celular', models.CharField(blank=True, max_length=13)),
                ('telefono', models.CharField(blank=True, max_length=10)),
                ('imagen', models.ImageField(blank=True, null=True, upload_to='usuarios/imagen_perfil/')),
                ('fecha_nacimiento', models.DateField(blank=True, null=True)),
                ('is_active', models.BooleanField(default=True)),
                ('is_staff', models.BooleanField(default=False)),
                ('is_admin', models.BooleanField(default=False)),
                ('creado', models.DateTimeField(auto_now_add=True)),
                ('modificado', models.DateTimeField(auto_now=True)),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.Group', verbose_name='groups')),
                ('pais_nacimiento', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='dashboard.Paises')),
                ('user_permissions', models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.Permission', verbose_name='user permissions')),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
