from django.db import models
from datetime import datetime

# Create your models here.

class Datos_Usuario(models.Model):
    nombre=models.CharField(max_length=1000)
    apellido=models.CharField(max_length=1000)
    fecha_nacimiento=models.CharField(max_length=10)
    id = models.AutoField(primary_key=True)
    usuario=models.CharField(max_length=100)
    gender = models.CharField(max_length=10, null=True)
    nacionality=models.CharField(max_length=100, null=True)

class Post(models.Model):
    texto=models.CharField(max_length=10000)
    id = models.AutoField(primary_key=True)
    usuario=models.CharField(max_length=100)
    date_created= models.DateTimeField(default=datetime.now,blank=True)


class Amigos(models.Model):
    id_usuario1=models.CharField(max_length=100000)
    id_usuario2=models.CharField(max_length=100000)
    estado=models.CharField(max_length=50)

class Likes(models.Model):
    id_publicacion=models.CharField(max_length=100000,null=True)
    id_usuario=models.CharField(max_length=100000,null=True)

class Comentarios(models.Model):
    id_publicacion=models.CharField(max_length=100000,null=True)
    texto=models.CharField(max_length=100000,null=True)
    id_usuario=models.CharField(max_length=100000,null=True)
    fecha_creacion=models.DateTimeField(default=datetime.now,blank=True)

class Mensajes(models.Model):
    mensaje=models.CharField(max_length=100000,null=True)
    usuario1=models.CharField(max_length=100000,null=True)
    usuario2=models.CharField(max_length=100000,null=True)
    fecha_creacion=models.DateTimeField(default=datetime.now,blank=True)
    leido=models.CharField(max_length=3,null=True)