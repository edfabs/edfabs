# Generated by Django 3.0.3 on 2020-08-05 21:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0014_post_header_image'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='header_image',
            field=models.ImageField(blank=True, null=True, upload_to='images/header_post/'),
        ),
    ]