# Generated by Django 3.0.3 on 2025-01-09 20:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('asambleas', '0004_auto_20250109_2022'),
    ]

    operations = [
        migrations.AlterField(
            model_name='trabajador',
            name='clave_centro_trabajo',
            field=models.CharField(max_length=50),
        ),
    ]
