# Generated by Django 3.0.3 on 2025-01-09 20:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('asambleas', '0003_auto_20250109_1952'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='trabajador',
            name='primer_apellido',
        ),
        migrations.RemoveField(
            model_name='trabajador',
            name='segundo_apellido',
        ),
        migrations.AlterField(
            model_name='trabajador',
            name='nombre',
            field=models.CharField(max_length=200),
        ),
    ]
