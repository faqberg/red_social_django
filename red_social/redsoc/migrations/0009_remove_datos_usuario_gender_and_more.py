# Generated by Django 5.0 on 2024-01-27 17:43

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('redsoc', '0008_remove_datos_usuario_genero_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='datos_usuario',
            name='gender',
        ),
        migrations.RemoveField(
            model_name='datos_usuario',
            name='nacionality',
        ),
    ]
