from django.shortcuts import render
from django.contrib import messages
from django.http import HttpResponseRedirect
from django.template import context
from .models import Publicacion, Grupo, Comentario, Skin, PrivacidadGrupo,UserGrupos, Permisos, Suscripcion, DenunciaUsuarios

from django.http import HttpResponse
from django.shortcuts import render, redirect
from .forms import SignupForm
from django.contrib.sites.shortcuts import get_current_site
from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.template.loader import render_to_string
from .tokens import account_activation_token
from django.core.mail import EmailMessage
from django.contrib.auth.forms import UserCreationForm 
from django.contrib.auth.models import (
    BaseUserManager, AbstractBaseUser
)
from .forms import NuevoGrupo, PublicacionForm
from django.core.files.storage import FileSystemStorage

from django.contrib.auth import authenticate, login
from django.contrib.auth import logout as django_logout
from django.contrib.auth import login as auth_login

from django.contrib.auth import get_user_model
User = get_user_model()

# Create your views here.

def inicio(request):
    listaPublicaciones = Publicacion.objects.filter(Estado = 1).order_by('-FechaPublicacion')
    listaGrupos = Grupo.objects.all().order_by('NombreGrupo')
    listaComentarios = Comentario.objects.all()
    listaSuscripciones = Suscripcion.objects.filter(Estado = 1).order_by('-fecha_peticion')
    formNuevoGrupo = NuevoGrupo()
    
    return render(request, 'adminlte/index.html',{'listaPublicaciones' : listaPublicaciones ,'listaGrupos': listaGrupos, 'formNuevoGrupo': formNuevoGrupo, 'listaComentarios': listaComentarios, 'listaSuscripciones': listaSuscripciones})


CRITICAL = 50
def login(request):
        if request.user.is_authenticated:
                return HttpResponseRedirect('/inicio/')
        else:
                if request.method == 'POST':
                        username = request.POST.get('username')
                        password = request.POST.get('password')
                        user = authenticate(request, username=username, password=password)
                        if user is not None:
                                auth_login(request , user)
                                return HttpResponseRedirect('/inicio/')
                        else:
                                messages.warning(request, u'Usuario o Contrase\xf1a incorrectos.') 
                                return render(request, 'adminlte/login.html' , {} )
                else: 
                        return render(request, 'adminlte/login.html' ,{} )
       

def logout(request):
    django_logout(request)
    return  HttpResponseRedirect('/login/')



def signup(request):
    if request.method == 'POST':
        form = SignupForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = False
            user.save()
            current_site = get_current_site(request)
            mail_subject = 'SarasaUCSE | Activacion Mail'
            message = render_to_string('acc_active_email.html', {
                'user': user,
                'domain': current_site.domain,
                'uid':urlsafe_base64_encode(force_bytes(user.pk)).decode(),
                'token': account_activation_token.make_token(user),
            })
            to_email = form.cleaned_data.get('email')
            email = EmailMessage(
                        mail_subject, message, to=[to_email]
            )
            email.send()
            valido = True
            return render(request, 'adminlte/signup.html', {'form': form, 'valido': valido})
    else:
        form = SignupForm()
    return render(request, 'adminlte/signup.html', {'form': form})

def activate(request, uidb64, token):
    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        instanciaSkin = Skin.objects.get(nombreSkin = 'skin-green')
        user.skinUser = instanciaSkin
        user.avatar = "https://i.imgur.com/AjJYeL2.png"
        user.save()
        auth_login(request, user)
        return HttpResponseRedirect('/')
        
    else:
        return HttpResponse('Link de activacion es invalidad!')


def publicar(request):

        if request.method == 'POST':
                contenido = request.POST.get('contenidoPublicacion')
                publicacion = Publicacion()

                publicacion.idUserPublico = request.user
                publicacion.Titulo = "Prueba"
                publicacion.Contenido = contenido
                publicacion.save()
                return HttpResponseRedirect('inicio/')
        else:
                publicaciones = Publicacion.objects.filter(Estado = 1).order_by('-FechaPublicacion')
                return render(request, 'adminlte/index.html', {listaPublicaciones : publicaciones})

def borrarPublicacion(request):
        if request.method == 'POST':
                pkPublicacion = request.POST.get('publicacionId')
                publicacion = Publicacion()
                publicacion = Publicacion.objects.get(idPublicacion = pkPublicacion)
                if request.user == publicacion.idUserPublico:
                        publicacion.Estado = 2
                        publicacion.save()
        publicaciones = Publicacion.objects.filter(Estado = 1).order_by('-FechaPublicacion')
        return render(request, 'adminlte/index.html', {'listaPublicaciones' : publicaciones})        


def guardarPublicacion(request):
        if request.method == 'POST':
                pkPublicacion = request.POST.get('publicacionId')
                contenido = request.POST.get('contenido')
                publicacion = Publicacion()
                publicacion = Publicacion.objects.get(idPublicacion = pkPublicacion)
                if request.user == publicacion.idUserPublico:
                        publicacion.Contenido = contenido
                        publicacion.save()
        publicaciones = Publicacion.objects.filter(Estado = 1).order_by('-FechaPublicacion')
        return render(request, 'adminlte/index.html', {'listaPublicaciones' : publicaciones})


def comentarPublicacion(request):
        if request.method == 'POST':
                pkPublicacion = request.POST.get('publicacionId')
                contenido = request.POST.get('contenido')
                comentario = Comentario()
                publicacion = Publicacion()
                publicacion = Publicacion.objects.get(idPublicacion = pkPublicacion)
                comentario.idPublicacionC = publicacion
                comentario.idUserComento = request.user
                comentario.ContenidoComentario = contenido
                comentario.save()
        publicaciones = Publicacion.objects.filter(Estado = 1).order_by('-FechaPublicacion')
        return render(request, 'adminlte/index.html', {'listaPublicaciones' : publicaciones})

def denunciarPublicacion(request):
        if request.method == 'POST':
                pkPublicacion = request.POST.get('id')
                contenido = request.POST.get('contenido')
                denunciaUsuario = DenunciaUsuarios()
                cantidad = DenunciaUsuarios.objects.filter(idUsuario = request.user, idPublicacion = pkPublicacion).count()
                
                if cantidad < 1:
                        publicacion = Publicacion()
                        publicacion = Publicacion.objects.get(idPublicacion = pkPublicacion)
                
                        denunciaUsuario = DenunciaUsuarios()
                        denunciaUsuario.idUsuario = request.user
                        denunciaUsuario.idPublicacion = publicacion
                        denunciaUsuario.Contenido = contenido
                        denunciaUsuario.save()

                        
                denuncias = DenunciaUsuarios.objects.filter(idPublicacion = pkPublicacion).count()
                if denuncias > 3:
                        publicacion.Estado = 2
                        
                        publicacion.save()        
                print(denuncias)

                data = {
                   'mensaje' : "Denuncia Exitosa"
                } 
        return JsonResponse(data)        

def grupos(request, pk=None):
        listaSuscripciones = Suscripcion.objects.filter(Estado = 1).order_by('-fecha_peticion')
        formNuevoGrupo = NuevoGrupo()
        
        if pk:
                
                miembros_grupos = []
                grupo = Grupo.objects.filter(idGrupo=pk)[0]
                for miembro_grupo in UserGrupos.objects.filter(idGrupoUsuario = grupo):
                   miembros_grupos.append(miembro_grupo.idUser)
                User = get_user_model()
                miembros = User.objects.filter(username__in = miembros_grupos)
                valido = False
                if request.user in miembros:
                        valido = True
                        
                publicaciones = Publicacion.objects.filter(idGrupoPu = pk)
                return render(request, 'adminlte/grupo_tema.html', {'grupo' : grupo, 'miembros' : miembros, 'publicaciones':publicaciones,'listaSuscripciones': listaSuscripciones, 'formNuevoGrupo': formNuevoGrupo, 'valido':valido })
        lista_gruposuser = UserGrupos.objects.all().filter(idUser=request.user)
        lista_Grupos = Grupo.objects.all().order_by('NombreGrupo')
        lista_grupos = []
        for grupo in lista_Grupos:
            for grupouser in lista_gruposuser:
                if grupo == grupouser.idGrupoUsuario:
                    lista_grupos.append(grupo)
        publicaciones = Publicacion.objects.all()
        return render(request, 'adminlte/grupos.html', {'lista_grupos' : lista_grupos,'publicaciones':publicaciones,'listaSuscripciones': listaSuscripciones, 'formNuevoGrupo': formNuevoGrupo})

def publicaciones(request, pk=None):
        publicacion = Publicacion.objects.get(idPublicacion = pk)
        comentarios = Comentario.objects.filter(idPublicacionC = publicacion.idPublicacion)
        return render(request, 'adminlte/publicacion.html', {'publicacion': publicacion, 'comentarios':comentarios} )
from django.urls import reverse
def grupo_publicacion(request, pk=None):
        grupo = Grupo.objects.filter(idGrupo = pk)[0]
        if request.method == 'POST':
                form = PublicacionForm(request.POST)
                if form.is_valid():
                        publicacion = form.save(commit=False)
                        publicacion.idUserPublico = request.user
                        publicacion.idGrupoPu = Grupo.objects.filter(idGrupo = pk)[0]
                        publicacion.save()
                        print(publicacion)
                return HttpResponseRedirect('/grupos/'+pk)
        if request.method == 'GET':
                formNuevaPublicacion = PublicacionForm()
                return render(request, 'adminlte/publicacion_grupo.html', {'formNuevaPublicacion':formNuevaPublicacion,'grupo':grupo})

def crear_grupo(request):
        if request.method == 'POST':
                nombreGrupo = request.POST.get('nombreGrupo')
                nivelAcceso = request.POST.get('nivelAcceso')
                grupo = Grupo()
                usergrupo = UserGrupos()
                privacidad = PrivacidadGrupo()
                privacidad = PrivacidadGrupo.objects.get(Privacidad = nivelAcceso)
                grupo.NombreGrupo = nombreGrupo
                grupo.NivelAcceso = privacidad
                grupo.Creador = request.user
                grupo.save()
               
                usergrupo.idGrupoUsuario = grupo
                usergrupo.idUser = grupo.Creador
                usergrupo.Permisos = Permisos.objects.get(NombrePerm = 'Administrador')
               
                usergrupo.save()
                return HttpResponseRedirect('/grupos/')

def grupos_tema(request):
        if request.method == 'GET':
                return render(request, 'adminlte/grupo_tema.html')

def agregar_miembro_grupo(request):
        if request.method == 'POST':
                pk = request.POST.get('id')
                suscripcion = Suscripcion.objects.get(idSuscripcion = pk)
                userGrupos = UserGrupos()
                userGrupos.idGrupoUsuario = suscripcion.idGrupoSuscribio
                userGrupos.idUser = suscripcion.emisor
                permiso = Permisos()
                permiso.NombrePerm = "usuario"
                permiso.save()
                userGrupos.Permisos = permiso
                userGrupos.save()
                data = {
                        'mensaje' : "Agregado Correctamente"
                        }
                suscripcion.Estado = 2
                suscripcion.save()
        return JsonResponse(data)  

from django.http import JsonResponse
from django.core import serializers

def suscribirUsuario(request):
        if request.method == 'POST':
                grupoId = request.POST.get('id')
                usuarioEmisor = request.user

                grupo = Grupo.objects.get(idGrupo = grupoId)

                suscripcion = Suscripcion()

                exist = Suscripcion.objects.filter(emisor = usuarioEmisor, idGrupoSuscribio = grupo )
                
                if len(exist) < 1:
                        suscripcion.emisor = usuarioEmisor
                        suscripcion.idGrupoSuscribio = grupo
                        suscripcion.receptor = grupo.Creador
                        suscripcion.save()

        return render(request, 'adminlte/grupos.html')


def perfil(request, pk=None):
        if pk:
                print(pk)
                user = User.objects.get(username =pk)
                listaPublicaciones = Publicacion.objects.filter( idUserPublico = user)
        return render(request, 'adminlte/perfil.html',{'listaPublicaciones' : listaPublicaciones})


def cambiarSkin(request):
        if request.method == 'POST':
                skin = request.POST.get('skin')
                usuario = request.user
                instanciaSkin = Skin.objects.get(nombreSkin = skin)
                usuario.skinUser = instanciaSkin
                usuario.save()
        return render(request, 'adminlte/index.html')


def cambiarFotoPerfil(request):
    if request.method == 'POST':
        usuario = request.user
        imagen = request.POST.get('imagen')
        usuario.avatar = imagen
        usuario.save()
    return render(request, 'adminlte/index.html')
                
#Api
from django.http import JsonResponse
from rest_framework import viewsets

from rest_framework.filters import OrderingFilter
from django_filters.rest_framework import DjangoFilterBackend

from .serializers import GrupoSerializer
from .serializers import UserSerializer
from .serializers import SuscripcionSerializer
from django.contrib.auth import get_user_model

def api_v1(request):
    return render(request, 'api_v1.html', {})

def api_cantidad_grupos(request):
    data = {
        'cantidad_grupos': Grupo.objects.count()
    }
    return JsonResponse(data)

class GrupoViewSet(viewsets.ModelViewSet):
    queryset = Grupo.objects.all().order_by('NombreGrupo')
    serializer_class = GrupoSerializer
    filter_backends = (OrderingFilter, DjangoFilterBackend)

class UserViewSet(viewsets.ModelViewSet):
        User = get_user_model()
        queryset = User.objects.all()
        serializer_class = UserSerializer
        filter_backends = (OrderingFilter, DjangoFilterBackend)

class SuscripcionViewSet(viewsets.ModelViewSet):
        queryset = Suscripcion.objects.all()
        serializer_class = SuscripcionSerializer
        filter_backends = (OrderingFilter, DjangoFilterBackend)
