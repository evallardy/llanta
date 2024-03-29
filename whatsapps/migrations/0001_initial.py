# Generated by Django 4.0.4 on 2024-02-07 22:08

import django.contrib.auth.mixins
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Bitacora',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('descripcion', models.CharField(max_length=255, verbose_name='Descripción')),
                ('fecha', models.DateTimeField(auto_now_add=True, verbose_name='Fecha')),
            ],
            options={
                'verbose_name': 'Registro',
                'verbose_name_plural': 'Registros',
                'db_table': 'Bitcora',
                'ordering': ['-fecha'],
            },
            bases=(models.Model, django.contrib.auth.mixins.PermissionRequiredMixin),
        ),
        migrations.CreateModel(
            name='MensajePicky',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('token', models.CharField(blank=True, max_length=255, null=True, verbose_name='Token')),
                ('number', models.CharField(max_length=50, verbose_name='Number')),
                ('message_in', models.CharField(max_length=255, verbose_name='Mensage in')),
                ('message_in_raw', models.CharField(max_length=255, verbose_name='Mensaje in raw')),
                ('message', models.CharField(blank=True, max_length=255, null=True, verbose_name='Mensaje')),
                ('application', models.CharField(blank=True, max_length=255, null=True, verbose_name='Aplicación')),
                ('tipo', models.CharField(default=2, max_length=255, verbose_name='Type')),
                ('unique_id', models.CharField(blank=True, max_length=255, null=True, verbose_name='Unique id')),
                ('quoted', models.CharField(blank=True, max_length=255, null=True, verbose_name='Quoted')),
                ('estatus_mensaje', models.IntegerField(choices=[(0, 'Terminado'), (1, 'Activo')], default=1, verbose_name='Estatus del mensaje')),
                ('fecha_alta', models.DateTimeField(auto_now_add=True, verbose_name='Fecha alta')),
                ('nivel', models.IntegerField(default=1, verbose_name='Nivel de pregunta')),
                ('opcion1', models.JSONField(blank=True, null=True, verbose_name='Bienvenida')),
                ('opcion2', models.JSONField(blank=True, null=True, verbose_name='Ancho')),
                ('opcion3', models.JSONField(blank=True, null=True, verbose_name='Alto')),
                ('opcion4', models.JSONField(blank=True, null=True, verbose_name='Rin')),
                ('opcion5', models.JSONField(blank=True, null=True, verbose_name='Opciones')),
                ('opcion6', models.JSONField(blank=True, null=True, verbose_name='Llantas')),
                ('opcion7', models.JSONField(blank=True, null=True, verbose_name='Envio')),
                ('opcion8', models.JSONField(blank=True, null=True, verbose_name='Correo')),
                ('opcion9', models.JSONField(blank=True, null=True, verbose_name='Adicional')),
            ],
            options={
                'verbose_name': 'Mensaje picky',
                'verbose_name_plural': 'Mensajes picky',
                'db_table': 'MensajePicky',
                'ordering': ['number', '-fecha_alta'],
            },
            bases=(models.Model, django.contrib.auth.mixins.PermissionRequiredMixin),
        ),
    ]
