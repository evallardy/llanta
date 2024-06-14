# Generated by Django 4.0.4 on 2023-05-18 22:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0002_bitacora_mensajepicky_llanta_alto_llanta_ancho_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='llanta',
            name='alto',
            field=models.CharField(blank=True, max_length=10, null=True, verbose_name='Alto'),
        ),
        migrations.AlterField(
            model_name='llanta',
            name='ancho',
            field=models.CharField(blank=True, max_length=10, null=True, verbose_name='Ancho'),
        ),
        migrations.AlterField(
            model_name='llanta',
            name='rin',
            field=models.CharField(blank=True, max_length=10, null=True, verbose_name='Rin'),
        ),
    ]