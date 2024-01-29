from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse
from django.contrib.auth.models import User, auth
from django.contrib import messages
from .models import Datos_Usuario,Post,Amigos,Likes,Comentarios,Mensajes
from django.contrib.auth.decorators import login_required
from datetime import datetime


# Create your views here.

def index(request):
    solicitudes_recibidas=Amigos.objects.filter(id_usuario2=request.user.id,estado="Pendiente").count()
    amigos1=Amigos.objects.filter(id_usuario1=request.user.id,estado="Aceptado").count()
    amigos2=Amigos.objects.filter(id_usuario2=request.user.id,estado="Aceptado").count()
    amigos_totales=amigos1+amigos2
    publicaciones=[]
    id_amigos1=Amigos.objects.filter(id_usuario1=request.user.id,estado="Aceptado").all()
    id_amigos2=Amigos.objects.filter(id_usuario2=request.user.id,estado="Aceptado").all()
    
    id_amigos=[]
    usuario_amigo=[]
    datos_amigos=[]
    for id_amigo in id_amigos1:
        id_amigos.append(id_amigo.id_usuario2)
    for id_amigo in id_amigos2:
        id_amigos.append(id_amigo.id_usuario1)
    
    for amigo in id_amigos:
        usuario_amigo.append(User.objects.filter(id=amigo).first().username)
    
    publicaciones1=Post.objects.filter(usuario=request.user.username).all()
    
    
    
    for publicacion in publicaciones1:
        publicaciones.append(publicacion)
    for amigo in usuario_amigo:
        publicaciones_amigo=Post.objects.filter(usuario=amigo).all()
        for publicacion in publicaciones_amigo:
            publicaciones.append(publicacion)

    publicaciones2=[]

    for elemento in publicaciones:
        publicaciones2.append(elemento.id)

    for publicacion in publicaciones:
        datos_amigos.append(Datos_Usuario.objects.filter(usuario=publicacion.usuario).first())
    print(publicaciones2)

    i=0
    for publicacion in publicaciones:
        liked="no"
        if Likes.objects.filter(id_usuario=request.user.id,id_publicacion=publicacion.id).exists():
            liked="si"
        numero_comentarios=Comentarios.objects.filter(id_publicacion=publicacion.id).count()
        numero_likes=Likes.objects.filter(id_publicacion=publicacion.id).count()
        publicacion.numero_comentarios=numero_comentarios
        publicacion.liked=liked
        publicacion.numero_likes=numero_likes
        publicacion.nombre=datos_amigos[i].nombre
        publicacion.apellido=datos_amigos[i].apellido
        i=i+1
    
    publicaciones = sorted(publicaciones, key=lambda x: x.date_created, reverse=True)
    
    
    return render(request,"index.html",{'solicitudes_recibidas':solicitudes_recibidas,'amigos_totales':amigos_totales,'datos_amigos':datos_amigos,'publicaciones':publicaciones})

def login(request):
    if request.method == 'POST':
        usuario=request.POST["username"]
        contra=request.POST["password"]
        if User.objects.filter(username=usuario).exists():
            user=auth.authenticate(username=usuario,password=contra)
            if user is not None:
                auth.login(request,user)
                return redirect("index")
            else:
                messages.info(request,"Credenciales inválidas")
                return redirect("login")
        else:
            messages.info(request,"El usuario indicado no existe.")
            return redirect("login")
        
    else:
        return render(request,"login.html")

def signin(request):
    if request.method=="POST":
        email=request.POST['email']
        usuario=request.POST["username"]
        contra=request.POST["password"]
        contra2=request.POST["confirm_password"]
        nombre=request.POST["name"]
        apellido=request.POST["last_name"]
        fecha_nacimiento=request.POST["birthdate"]
        if contra==contra2:
            if User.objects.filter(username=usuario).exists():
                messages.info(request,"Usuario ya en uso")
                return redirect("signin")
            elif User.objects.filter(email=email).exists():
                messages.info(request,"Email ya en uso")
                return redirect("signin")
            else:
                user = User.objects.create_user(username=usuario,email=email,password=contra)
                user.save()
                data_user=Datos_Usuario.objects.create(nombre=nombre,apellido=apellido,fecha_nacimiento=fecha_nacimiento,usuario=usuario)
                data_user.save()
                return redirect("login")
        else:
            messages.info(request,"Las contraseñas no coinciden")
            return redirect("signin")
    else:
        return render(request,"signin.html")

def logout(request):
    auth.logout(request)
    return redirect("/")

def createpost(request):
    if request.method=="POST":
        texto_publicacion=request.POST["texto_publicacion"]
        usuario_publicacion=request.user.username
        nuevo_post=Post.objects.create(texto=texto_publicacion,usuario=usuario_publicacion)
        nuevo_post.save()
        post_creado=Post.objects.filter(texto=texto_publicacion,usuario=usuario_publicacion).first()
        id_post=str(post_creado.id)
        return redirect("posts/"+id_post)

def createpost2(request):
    if request.method=="POST":
        texto_publicacion=request.POST["texto_publicacion"]
        usuario_publicacion=request.user.username
        nuevo_post=Post.objects.create(texto=texto_publicacion,usuario=usuario_publicacion)
        nuevo_post.save()
        post_creado=Post.objects.filter(texto=texto_publicacion,usuario=usuario_publicacion).first()
        id_post=str(post_creado.id)
        return redirect("perfil/"+usuario_publicacion)
    
def posts(request, id):
    publicacion=Post.objects.filter(id=id).first()
    texto_publicacion=publicacion.texto
    usuario_publicacion=publicacion.usuario
    fecha_publicacion=publicacion.date_created
    nombre_usuario=Datos_Usuario.objects.get(usuario=usuario_publicacion).nombre
    apellido_usuario=Datos_Usuario.objects.get(usuario=usuario_publicacion).apellido
    solicitudes_recibidas=Amigos.objects.filter(id_usuario2=request.user.id,estado="Pendiente").count()
    amigos1=Amigos.objects.filter(id_usuario1=request.user.id,estado="Aceptado").count()
    amigos2=Amigos.objects.filter(id_usuario2=request.user.id,estado="Aceptado").count()
    amigos_totales=amigos1+amigos2
    numero_likes=Likes.objects.filter(id_publicacion=id).count()
    liked="no"
    if Likes.objects.filter(id_publicacion=id,id_usuario=request.user.id).exists():
        liked="si"

    comentarios=Comentarios.objects.filter(id_publicacion=id).all()
    for comentario in comentarios:
        datos=Datos_Usuario.objects.get(usuario=User.objects.get(id=comentario.id_usuario).username)
        comentario.nombre=datos.nombre
        comentario.apellido=datos.apellido
        comentario.usuario=datos.usuario
    numero_comentarios=Comentarios.objects.filter(id_publicacion=id).count()
    return render(request,"post.html",{'texto_publicacion':texto_publicacion,'usuario_publicacion':usuario_publicacion,'id_publicacion':id,'fecha_publicacion':fecha_publicacion,'solicitudes_recibidas':solicitudes_recibidas,'amigos_totales':amigos_totales,'nombre_usuario':nombre_usuario,'apellido_usuario':apellido_usuario,'numero_likes':numero_likes,'liked':liked,'comentarios':comentarios,'numero_comentarios':numero_comentarios})

def perfil(request,user):
    usuario=Datos_Usuario.objects.filter(usuario=user).first()
    nombre_usuario=usuario.nombre
    apellido_usuario=usuario.apellido
    fecha_nacimiento_usuario=usuario.fecha_nacimiento
    id_usuario=User.objects.filter(username=user).first().id
    estado_amistad=Amigos.objects.filter(id_usuario1=request.user.id,id_usuario2=id_usuario).exists()
    estado_solicitud="No"
    recibido_enviado="No"
    if Amigos.objects.filter(id_usuario1=request.user.id,id_usuario2=id_usuario).exists() or Amigos.objects.filter(id_usuario2=request.user.id,id_usuario1=id_usuario).exists():
        if Amigos.objects.filter(id_usuario1=request.user.id,id_usuario2=id_usuario).exists():
            estado_solicitud=Amigos.objects.filter(id_usuario1=request.user.id,id_usuario2=id_usuario).first().estado
            recibido_enviado="enviado"
        if Amigos.objects.filter(id_usuario2=request.user.id,id_usuario1=id_usuario).exists():
            estado_solicitud=Amigos.objects.filter(id_usuario2=request.user.id,id_usuario1=id_usuario).first().estado
            recibido_enviado="recibido"
    
    solicitudes_recibidas=Amigos.objects.filter(id_usuario2=request.user.id,estado="Pendiente").count()
    amigos1=Amigos.objects.filter(id_usuario1=request.user.id,estado="Aceptado").count()
    amigos2=Amigos.objects.filter(id_usuario2=request.user.id,estado="Aceptado").count()
    amigos_totales=amigos1+amigos2

    posts = Post.objects.filter(usuario=user).all()
    


    for post in posts:
        cantidad_likes=Likes.objects.filter(id_publicacion=post.id).count()
        numero_comentarios=Comentarios.objects.filter(id_publicacion=post.id).count()
        post.cantidad_likes=cantidad_likes
        post.numero_comentarios=numero_comentarios
        if Likes.objects.filter(id_publicacion=post.id,id_usuario=request.user.id).exists():
            post.liked="si"
        else:
            post.liked="no"

    

    return render(request,"perfil.html",{'nombre_usuario':nombre_usuario,'apellido_usuario':apellido_usuario,'fecha_nacimiento_usuario':fecha_nacimiento_usuario,'usuario_perfil':user,'estado_solicitud':estado_solicitud,'recibido_enviado':recibido_enviado,'solicitudes_recibidas':solicitudes_recibidas,'amigos_totales':amigos_totales,'posts':posts,})

def perfil_amigos_info(request,user,seccion):
    usuario=Datos_Usuario.objects.filter(usuario=user).first()
    nombre_usuario=usuario.nombre
    apellido_usuario=usuario.apellido
    fecha_nacimiento_usuario=usuario.fecha_nacimiento
    id_usuario=User.objects.filter(username=user).first().id
    genero_usuario=usuario.gender
    nacionalidad_usuario=usuario.nacionality
    email_usuario=User.objects.filter(username=user).first().email
    if genero_usuario is None:
        genero_usuario="-"
    if nacionalidad_usuario is None:
        nacionalidad_usuario="-"
    estado_amistad=Amigos.objects.filter(id_usuario1=request.user.id,id_usuario2=id_usuario).exists()
    estado_solicitud="No"
    recibido_enviado="No"
    if Amigos.objects.filter(id_usuario1=request.user.id,id_usuario2=id_usuario).exists() or Amigos.objects.filter(id_usuario2=request.user.id,id_usuario1=id_usuario).exists():
        if Amigos.objects.filter(id_usuario1=request.user.id,id_usuario2=id_usuario).exists():
            estado_solicitud=Amigos.objects.filter(id_usuario1=request.user.id,id_usuario2=id_usuario).first().estado
            recibido_enviado="enviado"
        if Amigos.objects.filter(id_usuario2=request.user.id,id_usuario1=id_usuario).exists():
            estado_solicitud=Amigos.objects.filter(id_usuario2=request.user.id,id_usuario1=id_usuario).first().estado
            recibido_enviado="recibido"
    
    solicitudes_recibidas=Amigos.objects.filter(id_usuario2=request.user.id,estado="Pendiente").count()
    amigos1=Amigos.objects.filter(id_usuario1=request.user.id,estado="Aceptado").count()
    amigos2=Amigos.objects.filter(id_usuario2=request.user.id,estado="Aceptado").count()
    amigos_totales=amigos1+amigos2

    lista_amigos=[]

    lista_amigos1=Amigos.objects.filter(id_usuario1=id_usuario,estado="Aceptado").all()
    for amigo in lista_amigos1:
        lista_amigos.append(Datos_Usuario.objects.get(usuario=User.objects.get(id=amigo.id_usuario2).username))

    lista_amigos2=Amigos.objects.filter(id_usuario2=id_usuario,estado="Aceptado").all()
    for amigo in lista_amigos2:
        lista_amigos.append(Datos_Usuario.objects.get(usuario=User.objects.get(id=amigo.id_usuario1).username))

    
    return render(request,"perfil_amigos_info.html",{'nombre_usuario':nombre_usuario,'apellido_usuario':apellido_usuario,'fecha_nacimiento_usuario':fecha_nacimiento_usuario,'usuario_perfil':user,'genero_usuario':genero_usuario,'nacionalidad_usuario':nacionalidad_usuario,'email_usuario':email_usuario,'estado_solicitud':estado_solicitud,'recibido_enviado':recibido_enviado,'solicitudes_recibidas':solicitudes_recibidas,'amigos_totales':amigos_totales,'lista_amigos':lista_amigos,'seccion':seccion})


def agregar_amigo(request):
    usuario_perfil=request.POST["usuario_perfil"]
    usuario_perfil2=User.objects.filter(username=usuario_perfil).first()
    id_usuario_perfil=usuario_perfil2.id
    id_propio=request.user.id
    solicitud=Amigos.objects.create(id_usuario1=id_propio,id_usuario2=id_usuario_perfil,estado="Pendiente")
    solicitud.save()
    return redirect("perfil/"+usuario_perfil)

def eliminar_solicitud_amistad(request):
    usuario_perfil=request.POST["usuario_perfil"]
    usuario_perfil2=User.objects.filter(username=usuario_perfil).first()
    id_usuario_perfil=usuario_perfil2.id
    id_propio=request.user.id
    solicitud_enviada=Amigos.objects.get(id_usuario1=id_propio,id_usuario2=id_usuario_perfil)
    solicitud_enviada.delete()
    return redirect("perfil/"+usuario_perfil)

def aceptar_solicitud_amistad(request):
    usuario_perfil=request.POST["usuario_perfil"]
    usuario_perfil2=User.objects.filter(username=usuario_perfil).first()
    id_usuario_perfil=usuario_perfil2.id
    id_propio=request.user.id
    solicitud_recibida=Amigos.objects.get(id_usuario2=id_propio,id_usuario1=id_usuario_perfil)
    solicitud_recibida.estado="Aceptado"
    solicitud_recibida.save()
    return redirect("perfil/"+usuario_perfil)

def eliminar_solicitud_amistad2(request):
    usuario_perfil=request.POST["usuario_perfil"]
    usuario_perfil2=User.objects.filter(username=usuario_perfil).first()
    id_usuario_perfil=usuario_perfil2.id
    id_propio=request.user.id
    solicitud_enviada=Amigos.objects.get(id_usuario2=id_propio,id_usuario1=id_usuario_perfil)
    solicitud_enviada.delete()
    return redirect("solicitudes_amistad")

def eliminar_solicitud_amistad3(request):
    usuario_perfil=request.POST["usuario_perfil"]
    usuario_perfil2=User.objects.filter(username=usuario_perfil).first()
    id_usuario_perfil=usuario_perfil2.id
    id_propio=request.user.id
    solicitud_enviada=Amigos.objects.get(id_usuario1=id_propio,id_usuario2=id_usuario_perfil)
    solicitud_enviada.delete()
    return redirect("solicitudes_amistad/?q=enviadas")

def aceptar_solicitud_amistad2(request):
    usuario_perfil=request.POST["usuario_perfil"]
    usuario_perfil2=User.objects.filter(username=usuario_perfil).first()
    id_usuario_perfil=usuario_perfil2.id
    id_propio=request.user.id
    solicitud_recibida=Amigos.objects.get(id_usuario2=id_propio,id_usuario1=id_usuario_perfil)
    solicitud_recibida.estado="Aceptado"
    solicitud_recibida.save()
    return redirect("solicitudes_amistad")

def eliminar_amigo(request):
    usuario_perfil=request.POST["usuario_perfil"]
    usuario_perfil2=User.objects.filter(username=usuario_perfil).first()
    id_usuario_perfil=usuario_perfil2.id
    id_propio=request.user.id
    if Amigos.objects.filter(id_usuario1=id_usuario_perfil,id_usuario2=id_propio).exists():
        eliminar_solicitud=Amigos.objects.get(id_usuario1=id_usuario_perfil,id_usuario2=id_propio)
        eliminar_solicitud.delete()
        return redirect("perfil/"+usuario_perfil)
    else:
        eliminar_solicitud=Amigos.objects.get(id_usuario1=id_propio,id_usuario2=id_usuario_perfil)
        eliminar_solicitud.delete()
        return redirect("perfil/"+usuario_perfil)

def buscar(request):
    busqueda=request.GET.get("busqueda")
    categoria=request.GET.get("cat")
    if categoria=="usuario":
        if Datos_Usuario.objects.filter(usuario__contains=busqueda).exists():
            data=Datos_Usuario.objects.filter(usuario__contains=busqueda).all()
            print(data)
        else:
            data="No se encontraron resultados."
    elif categoria=="nombre_apellido":
        if Datos_Usuario.objects.filter(nombre__contains=busqueda).exists() or Datos_Usuario.objects.filter(apellido__contains=busqueda).exists():
            
            if Datos_Usuario.objects.filter(nombre__contains=busqueda).exists():
                print("si")
                data=Datos_Usuario.objects.filter(nombre__contains=busqueda).all()
                print(data)
                print("si")
            if Datos_Usuario.objects.filter(apellido__contains=busqueda).exists():
                data=Datos_Usuario.objects.filter(apellido__contains=busqueda).all()
        else:
            data="No se encontraron resultados."
    elif categoria=="publicaciones":
        if Post.objects.filter(texto__contains=busqueda).exists():
            datos_usuarios=[]
            data=Post.objects.filter(texto__contains=busqueda).all()
            for item in data:
                datos_usuarios.append(Datos_Usuario.objects.get(usuario=User.objects.get(username=item.usuario)))
            i=0
            for item in data:
                item.nombre=datos_usuarios[i].nombre
                item.apellido=datos_usuarios[i].apellido
                i=i+1
        else:
            data="No se encontraron resultados."

        
    solicitudes_recibidas=Amigos.objects.filter(id_usuario2=request.user.id,estado="Pendiente").count()
    amigos1=Amigos.objects.filter(id_usuario1=request.user.id,estado="Aceptado").count()
    amigos2=Amigos.objects.filter(id_usuario2=request.user.id,estado="Aceptado").count()
    amigos_totales=amigos1+amigos2
        
    return render(request,"buscar.html",{'busqueda':busqueda,'categoria':categoria,'data':data,'solicitudes_recibidas':solicitudes_recibidas,'amigos_totales':amigos_totales})

def amigos(request):
    solicitudes_recibidas=Amigos.objects.filter(id_usuario2=request.user.id,estado="Pendiente").count()
    amigos1=Amigos.objects.filter(id_usuario1=request.user.id,estado="Aceptado").count()
    amigos2=Amigos.objects.filter(id_usuario2=request.user.id,estado="Aceptado").count()
    amigos_totales=amigos1+amigos2
    amigos="Usted no tiene amigos agregados."
    if Amigos.objects.filter(id_usuario1=request.user.id,estado="Aceptado").exists() or Amigos.objects.filter(id_usuario2=request.user.id,estado="Aceptado").exists():
        amigos1=[]
        amigos=[]
        
        if Amigos.objects.filter(id_usuario1=request.user.id,estado="Aceptado").exists():
            usuario_amigo1=Amigos.objects.filter(id_usuario1=request.user.id,estado="Aceptado").all()
            for usuario in usuario_amigo1:
                amigos1.append(User.objects.get(id=usuario.id_usuario2).username)
            
            

        if Amigos.objects.filter(id_usuario2=request.user.id,estado="Aceptado").exists():
            usuario_amigo2=Amigos.objects.filter(id_usuario2=request.user.id,estado="Aceptado").all()
            for usuario in usuario_amigo2:
                amigos1.append(User.objects.get(id=usuario.id_usuario1).username)
        
        print(amigos1)
        
        for amigo in amigos1:
            amigos.append(Datos_Usuario.objects.get(usuario=amigo))

        
        

    return render(request,"amigos.html",{'solicitudes_recibidas':solicitudes_recibidas,'amigos_totales':amigos_totales,'amigos':amigos})

def solicitudes_amistad(request):
    
    if request.method == "GET":
        enviadas_recibidas = request.GET.get("q")
        if enviadas_recibidas is None:
            enviadas_recibidas = "recibidas"
    print(enviadas_recibidas)
    solicitudes_recibidas=Amigos.objects.filter(id_usuario2=request.user.id,estado="Pendiente").count()
    solicitudes_enviadas=Amigos.objects.filter(id_usuario1=request.user.id,estado="Pendiente").count()
    amigos1=Amigos.objects.filter(id_usuario1=request.user.id,estado="Aceptado").count()
    amigos2=Amigos.objects.filter(id_usuario2=request.user.id,estado="Aceptado").count()
    amigos_totales=amigos1+amigos2
    solicitudes_amistad_recibidas=[]
    solicitudes_amistad_enviadas=[]
    if solicitudes_recibidas > 0:
        sol_rec=Amigos.objects.filter(id_usuario2=request.user.id,estado="Pendiente").all()
        for x in sol_rec:
            usuario_que_envia=User.objects.filter(id=x.id_usuario1).first().username
            solicitudes_amistad_recibidas.append(Datos_Usuario.objects.filter(usuario=usuario_que_envia).first())

    if solicitudes_enviadas > 0:
        sol_env=Amigos.objects.filter(id_usuario1=request.user.id,estado="Pendiente").all()
        for x in sol_env:
            usuario_que_recibe=User.objects.filter(id=x.id_usuario2).first().username
            solicitudes_amistad_enviadas.append(Datos_Usuario.objects.filter(usuario=usuario_que_recibe).first())
    return render(request,"solicitudes_amistad.html",{"solicitudes_recibidas":solicitudes_recibidas,"amigos_totales":amigos_totales,'solicitudes_amistad_recibidas':solicitudes_amistad_recibidas,'solicitudes_amistad_enviadas':solicitudes_amistad_enviadas,'enviadas_recibidas':enviadas_recibidas})

def eliminar_post(request):
    id_post = request.POST["id_post"]
    perfil = request.POST["perfil"]
    post=Post.objects.get(id=id_post)
    post.delete()
    return redirect("perfil/"+perfil)

def eliminar_post2(request):
    id_post = request.POST["id_post"]
    
    post=Post.objects.get(id=id_post)
    post.delete()
    return redirect("index")

def editar_datos(request):
    usuario=Datos_Usuario.objects.get(usuario=request.user.username)
    email_usuario=User.objects.get(username=request.user.username).email
    nombre_usuario=usuario.nombre
    apellido_usuario=usuario.apellido
    fecha_nacimiento_usuario=usuario.fecha_nacimiento
    genero_usuario=usuario.gender
    nacionalidad_usuario=usuario.nacionality
    solicitudes_recibidas=Amigos.objects.filter(id_usuario2=request.user.id,estado="Pendiente").count()
    amigos1=Amigos.objects.filter(id_usuario1=request.user.id,estado="Aceptado").count()
    amigos2=Amigos.objects.filter(id_usuario2=request.user.id,estado="Aceptado").count()
    amigos_totales=amigos1+amigos2
    return render(request,"editar_datos.html",{'usuario':usuario,'email_usuario':email_usuario,'fecha_nacimiento_usuario':fecha_nacimiento_usuario,'genero_usuario':genero_usuario,'nacionalidad_usuario':nacionalidad_usuario,'nombre_usuario':nombre_usuario,'apellido_usuario':apellido_usuario,'amigos_totales':amigos_totales,'solicitudes_recibidas':solicitudes_recibidas,})

def editar_datos_action(request):
    
    usuario_post=request.POST["usuario_orig"]
    print(usuario_post)
    email_post=request.POST["email_orig"]
    usuario_cambio=request.POST["usuario_new"]
    email_cambio=request.POST["email"]
    genero_cambio=request.POST.get("genero")
    nacionalidad_cambio=request.POST.get("nacionalidad")
    print(nacionalidad_cambio)
    usuario=Datos_Usuario.objects.get(usuario=usuario_post)
    usuario.nombre=request.POST["nombre"]
    usuario.apellido=request.POST["apellido"]
    usuario.gender=genero_cambio
    usuario.nacionality=nacionalidad_cambio
    
    
    if usuario.save():
        print("SI")
    if usuario_post != usuario_cambio and User.objects.filter(username=usuario_cambio).exists():
        messages.info(request,"El usuario que ingresó ya está en uso.")
        return redirect("editar_datos")
    else:
        
        usuario.usuario=usuario_cambio
        usuario.save()
        usuario_nuevo=User.objects.get(username=usuario_post)
        contra=usuario_nuevo.password
        
        usuario_nuevo.username=usuario_cambio
        usuario_nuevo.save()
       
        posts_cambios=Post.objects.filter(usuario=usuario_post).all()
        for post in posts_cambios:
            post.usuario=usuario_cambio
            post.save()
           
        user=auth.authenticate(username=usuario_cambio,password=contra)
        auth.login(request,user)
        
    
    if email_post != email_cambio and User.objects.filter(email=email_cambio).exists():
        messages.info(request,"El email que ingresó ya está en uso.")
        return redirect("editar_datos")
    else:
        
        usuario_nuevo=User.objects.get(email=email_post)
        usuario_nuevo.email=email_cambio
        usuario_nuevo.save()
    
    messages.info(request,"Los cambios se guardaron con éxito.")

    return redirect("editar_datos")
    
        
def dar_like(request):
    id_publicacion=request.POST["id_publicacion"]
    id_usuario_like=request.user.id
    
    
    
    like=Likes.objects.create(id_publicacion=id_publicacion,id_usuario=id_usuario_like)
    like.save()
    return redirect("posts/"+id_publicacion)

def quitar_like(request):
    id_publicacion=request.POST["id_publicacion"]
    id_usuario_like=request.user.id
    
    
    like=Likes.objects.filter(id_publicacion=id_publicacion,id_usuario=id_usuario_like).first()
    like.delete()
    return redirect("posts/"+id_publicacion)

def comentar(request):
    texto_comentario=request.POST["texto_comentario"]
    id_usuario=request.user.id
    id_publicacion=request.POST["id_publicacion"]
    comentario=Comentarios.objects.create(id_publicacion=id_publicacion,id_usuario=id_usuario,texto=texto_comentario)
    comentario.save()
    return redirect("posts/"+id_publicacion)

def eliminar_comentario(request):
    
    id_post=request.POST["id_publicacion"]
    id_comentario=request.POST["id_comentario"]
    comentario=Comentarios.objects.get(id=id_comentario)
    comentario.delete()
    return redirect("posts/"+id_post)

def mensajes(request):
    solicitudes_recibidas=Amigos.objects.filter(id_usuario2=request.user.id,estado="Pendiente").count()
    amigos1=Amigos.objects.filter(id_usuario1=request.user.id,estado="Aceptado").count()
    amigos2=Amigos.objects.filter(id_usuario2=request.user.id,estado="Aceptado").count()
    amigos_totales=amigos1+amigos2
    if Mensajes.objects.filter(usuario1=request.user.username).count() + Mensajes.objects.filter(usuario2=request.user.username).count() == 0:
        conversaciones_datos="Usted no inició ninguna conversación."
    else:
        conversaciones=[]
        conversaciones1=Mensajes.objects.filter(usuario1=request.user.username).all()
        conversaciones2=Mensajes.objects.filter(usuario2=request.user.username).all()
        for conversacion in conversaciones1:
            conversacion.chat_con=conversacion.usuario2
            conversaciones.append(conversacion.chat_con)
        for conversacion in conversaciones2:
            conversacion.chat_con=conversacion.usuario1
            conversaciones.append(conversacion.chat_con)
        conversaciones=list(set(conversaciones))
        conversaciones_datos=[]
        for conversacion in conversaciones:
            conversaciones_datos.append({'usuario':conversacion,'nombre_apellido':""})
        
        for data in conversaciones_datos:
            data["nombre_apellido"]=Datos_Usuario.objects.get(usuario=data["usuario"]).nombre + " " +Datos_Usuario.objects.get(usuario=data["usuario"]).apellido
        

        

        for conversacion in conversaciones_datos:
            usuario_conversacion=conversacion["usuario"]
            nombre_apellido_usuario_conversacion=conversacion["nombre_apellido"]
            mensajes1=Mensajes.objects.filter(usuario1=request.user.username,usuario2=usuario_conversacion).all()
            mensajes2=Mensajes.objects.filter(usuario2=request.user.username,usuario1=usuario_conversacion).all()

            texto_mensajes=[]
            for mensaje in mensajes1:
                texto_mensajes.append({'texto_mensaje':mensaje.mensaje,'leido':mensaje.leido,'fecha':mensaje.fecha_creacion,'usuario1':mensaje.usuario1})
            for mensaje in mensajes2:
                texto_mensajes.append({'texto_mensaje':mensaje.mensaje,'leido':mensaje.leido,'fecha':mensaje.fecha_creacion,'usuario1':mensaje.usuario1})
            lista_ordenada = sorted(texto_mensajes, key=lambda x: x['fecha'], reverse=True)

            mensaje_mas_reciente={
            'mensaje':lista_ordenada[0]["texto_mensaje"],
            'leido':lista_ordenada[0]["leido"],
            'fecha_ultimo_mensaje':lista_ordenada[0]["fecha"],
            'usuario_ultimo_mensaje':lista_ordenada[0]["usuario1"]
            }
            conversacion["ultimo_mensaje"]=mensaje_mas_reciente["mensaje"]
            conversacion["ultimo_mensaje_leido"]=mensaje_mas_reciente["leido"]
            conversacion["fecha_ultimo_mensaje"]=mensaje_mas_reciente["fecha_ultimo_mensaje"]
            conversacion["usuario_ultimo_mensaje"]=mensaje_mas_reciente["usuario_ultimo_mensaje"]
    
    
    return render(request,"mensajes.html",{'solicitudes_recibidas':solicitudes_recibidas,'amigos_totales':amigos_totales,'conversaciones_datos':conversaciones_datos})

def chat(request,usuario):
    solicitudes_recibidas=Amigos.objects.filter(id_usuario2=request.user.id,estado="Pendiente").count()
    amigos1=Amigos.objects.filter(id_usuario1=request.user.id,estado="Aceptado").count()
    amigos2=Amigos.objects.filter(id_usuario2=request.user.id,estado="Aceptado").count()
    amigos_totales=amigos1+amigos2
    datos_usuario=Datos_Usuario.objects.get(usuario=usuario)
    
    return render(request,"enviar_mensajes.html",{'usuario':usuario,'solicitudes_recibidas':solicitudes_recibidas,'amigos_totales':amigos_totales,'datos_usuario':datos_usuario})

def send(request):
        message=request.POST["message"]
        usuario1=request.user.username
        usuario2=request.POST["usuario2"]
        

        new_message=Mensajes.objects.create(mensaje=message,usuario1=usuario1,usuario2=usuario2,leido="no")
        new_message.save()
        return HttpResponse("Message sent succesfully!")
    

def getMessages(request,usuario):
        # room_details=Room.objects.get(name=room)
        # messages=Message.objects.filter(room=room_details.id)
        messages=Mensajes.objects.filter(usuario2=usuario,usuario1=request.user.username)
        messages2=Mensajes.objects.filter(usuario1=usuario,usuario2=request.user.username)
        messages=messages.union(messages2)
        ultimo_msg=messages.last()
        if ultimo_msg.usuario2 == request.user.username:
            ultimo_msg.leido="si"
            ultimo_msg.save()
       
        
        return JsonResponse({"messages":list(messages.values())})
