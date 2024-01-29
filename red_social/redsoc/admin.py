from django.contrib import admin
from .models import Post, Datos_Usuario,Amigos,Likes,Comentarios,Mensajes

# Register your models here.

admin.site.register(Post)
admin.site.register(Datos_Usuario)
admin.site.register(Amigos)
admin.site.register(Likes)
admin.site.register(Comentarios)
admin.site.register(Mensajes)