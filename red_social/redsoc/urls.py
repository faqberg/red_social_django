from django.urls import path
from . import views

urlpatterns=[
    path("",views.index,name="index"),
    path("index",views.index),
    path("login",views.login,name="login"),
    path("signin",views.signin,name="signin"),
    path("logout",views.logout,name="logout"),
    path("createpost",views.createpost,name="createpost"),
    path("createpost2",views.createpost2,name="createpost2"),
    path("posts/<str:id>",views.posts,name="posts"),
    path("perfil/<str:user>",views.perfil,name="perfil"),
    path("perfil/<str:user>/<str:seccion>",views.perfil_amigos_info,name="perfil_amigos_info"),
    path("agregar_amigo",views.agregar_amigo,name="agregar_amigo"),
    path("mensajes",views.mensajes,name="mensajes"),
    path("chat/<str:usuario>",views.chat,name="chat"),
    path("eliminar_solicitud_amistad",views.eliminar_solicitud_amistad,name="eliminar_solicitud_amistad"),
    path("aceptar_solicitud_amistad",views.aceptar_solicitud_amistad,name="aceptar_solicitud_amistad"),
    path("eliminar_solicitud_amistad2",views.eliminar_solicitud_amistad2,name="eliminar_solicitud_amistad2"),
    path("eliminar_solicitud_amistad3",views.eliminar_solicitud_amistad3,name="eliminar_solicitud_amistad3"),
    path("aceptar_solicitud_amistad2",views.aceptar_solicitud_amistad2,name="aceptar_solicitud_amistad2"),
    path("eliminar_amigo",views.eliminar_amigo,name="eliminar_amigo"),
    path("solicitudes_amistad/",views.solicitudes_amistad,name="solicitudes_amistad"),
    path("amigos",views.amigos,name="amigos"),
    path("buscar",views.buscar,name="buscar"),
    path("eliminar_post",views.eliminar_post,name="eliminar_post"),
    path("eliminar_post2",views.eliminar_post2,name="eliminar_post2"),
    path("editar_datos",views.editar_datos,name="editar_datos"),
    path("editar_datos_action",views.editar_datos_action,name="editar_datos_action"),
    path("dar_like",views.dar_like,name="dar_like"),
    path("quitar_like",views.quitar_like,name="quitar_like"),
    path("comentar",views.comentar,name="comentar"),
    path("eliminar_comentario",views.eliminar_comentario,name="eliminar_comentario"),
    path("send",views.send,name="send"),
    path("getMessages/<str:usuario>/",views.getMessages,name="getMessages"),
    
    
]