# Generated by Django 3.0.3 on 2025-01-09 18:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('asambleas', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='asamblea',
            name='link',
            field=models.CharField(max_length=200),
        ),
    ]
