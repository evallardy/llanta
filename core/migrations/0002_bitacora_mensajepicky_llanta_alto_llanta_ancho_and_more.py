# Generated by Django 4.0.4 on 2023-05-18 20:55

import django.contrib.auth.mixins
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0001_initial'),
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
                ('opcion1', models.JSONField(blank=True, null=True, verbose_name='Acción')),
                ('opcion2', models.JSONField(blank=True, null=True, verbose_name='Bien')),
                ('opcion3', models.JSONField(blank=True, null=True, verbose_name='Estado')),
                ('opcion4', models.JSONField(blank=True, null=True, verbose_name='Municipio')),
                ('opcion5', models.JSONField(blank=True, null=True, verbose_name='Bien seleccionado')),
            ],
            options={
                'verbose_name': 'Mensaje picky',
                'verbose_name_plural': 'Mensajes picky',
                'db_table': 'MensajePicky',
                'ordering': ['number', '-fecha_alta'],
            },
            bases=(models.Model, django.contrib.auth.mixins.PermissionRequiredMixin),
        ),
        migrations.AddField(
            model_name='llanta',
            name='alto',
            field=models.CharField(blank=True, max_length=4, null=True, verbose_name='Alto'),
        ),
        migrations.AddField(
            model_name='llanta',
            name='ancho',
            field=models.CharField(blank=True, max_length=4, null=True, verbose_name='Ancho'),
        ),
        migrations.AddField(
            model_name='llanta',
            name='marca',
            field=models.CharField(blank=True, max_length=100, null=True, verbose_name='Marca'),
        ),
        migrations.AddField(
            model_name='llanta',
            name='radial',
            field=models.IntegerField(default=0, verbose_name='Radial'),
        ),
        migrations.AddField(
            model_name='llanta',
            name='rin',
            field=models.CharField(blank=True, max_length=4, null=True, verbose_name='Rin'),
        ),
        migrations.AlterField(
            model_name='llanta',
            name='actualizado',
            field=models.IntegerField(default=1, verbose_name='Actualizado en el proceso de extracción'),
        ),
        migrations.AlterField(
            model_name='llanta',
            name='afiliado',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=10, verbose_name='Afiliado'),
        ),
        migrations.AlterField(
            model_name='llanta',
            name='envio',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=10, verbose_name='Envio'),
        ),
        migrations.AlterField(
            model_name='llanta',
            name='utilidad',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=10, verbose_name='Utilidad'),
        ),
    ]
