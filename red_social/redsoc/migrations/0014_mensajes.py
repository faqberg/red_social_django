# Generated by Django 5.0 on 2024-01-29 04:14

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('redsoc', '0013_comentarios_fecha_creacion'),
    ]

    operations = [
        migrations.CreateModel(
            name='Mensajes',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('mensaje', models.CharField(max_length=100000, null=True)),
                ('usuario1', models.CharField(max_length=100000, null=True)),
                ('usuario2', models.CharField(max_length=100000, null=True)),
                ('fecha_creacion', models.DateTimeField(blank=True, default=datetime.datetime.now)),
            ],
        ),
    ]
