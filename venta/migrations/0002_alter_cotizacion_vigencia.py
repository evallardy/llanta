# Generated by Django 4.0.4 on 2024-01-31 19:01

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('venta', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cotizacion',
            name='vigencia',
            field=models.DateTimeField(default=datetime.datetime(2024, 3, 31, 19, 1, 19, 568091), verbose_name='Vigencia'),
        ),
    ]
