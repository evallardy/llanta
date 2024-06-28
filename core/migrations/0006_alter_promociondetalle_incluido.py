# Generated by Django 4.0.4 on 2024-06-25 22:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0005_alter_promociondetalle_unique_together'),
    ]

    operations = [
        migrations.AlterField(
            model_name='promociondetalle',
            name='incluido',
            field=models.IntegerField(choices=[(0, 'No'), (1, 'Si')], default=1, verbose_name='Incluido'),
        ),
    ]
