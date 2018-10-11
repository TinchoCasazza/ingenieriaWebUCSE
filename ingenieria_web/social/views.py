from django.shortcuts import render
from django.contrib import messages
from django.http import HttpResponseRedirect
from django.template import context
from .models import Publicacion, Grupo, Comentario, Skin, PrivacidadGrupo,UserGrupos, Permisos, Suscripcion

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
from .forms import NuevoGrupo
from django.core.files.storage import FileSystemStorage

from django.contrib.auth import authenticate, login
from django.contrib.auth import logout as django_logout
from django.contrib.auth import login as auth_login

from django.contrib.auth import get_user_model
User = get_user_model()

# Create your views here.

def inicio(request):
    listaPublicaciones = Publicacion.objects.all().order_by('-FechaPublicacion')
    listaGrupos = Grupo.objects.all().order_by('NombreGrupo')
    formNuevoGrupo = NuevoGrupo()
    return render(request, 'adminlte/index.html',{'listaPublicaciones' : listaPublicaciones ,'listaGrupos': listaGrupos, 'formNuevoGrupo': formNuevoGrupo})


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
                publicaciones = Publicacion.objects.all().order_by('-FechaPublicacion')
                return render(request, 'adminlte/index.html', {listaPublicaciones : publicaciones})

def borrarPublicacion(request):
        if request.method == 'POST':
                pkPublicacion = request.POST.get('publicacionId')
                publicacion = Publicacion()
                publicacion = Publicacion.objects.get(idPublicacion = pkPublicacion)
                estado = EstadoPublicacion.objects.get(NombreEstado = 'Eliminado')
                if request.user == publicacion.idUserPublico:
                        publicacion.Estado = estado
                        publicacion.save()
        publicaciones = Publicacion.objects.all().order_by('-FechaPublicacion')
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
        publicaciones = Publicacion.objects.all().order_by('-FechaPublicacion')
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
        publicaciones = Publicacion.objects.all().order_by('-FechaPublicacion')
        return render(request, 'adminlte/index.html', {'listaPublicaciones' : publicaciones})


def grupos(request, pk=None):
        if pk:
                return HttpResponse("grupo" + pk)
        lista_gruposuser = UserGrupos.objects.all().filter(idUser=request.user)
        lista_Grupos = Grupo.objects.all().order_by('NombreGrupo')
        lista_grupos = []
        for grupo in lista_Grupos:
            for grupouser in lista_gruposuser:
                if grupo == grupouser.idGrupoUsuario:
                    lista_grupos.append(grupo)

        return render(request, 'adminlte/grupos.html', {'lista_grupos' : lista_grupos})

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
                
from django.http import JsonResponse
from django.core import serializers

def suscribirUsuario(request):
        if request.method == 'GET':
                suscripciones = Suscripcion.objects.all()
                jsondata = serializers.serialize('json', suscripciones)
                return JsonResponse(jsondata , safe=False)
        if request.method == 'POST':
                grupoId = request.POST.get('id')
                usuarioEmisor = request.user

                grupo = Grupo.objects.get(idGrupo = grupoId)

                suscripcion = Suscripcion()

                suscripcion.emisor = usuarioEmisor
                suscripcion.idGrupoSuscribio = grupo
                suscripcion.receptor = grupo.Creador

                suscripcion.save()
        return render(request, 'adminlte/grupos.html')


def perfil(request):
        return render(request, 'adminlte/perfil.html')


def cambiarSkin(request):
        if request.method == 'POST':
                skin = request.POST.get('skin')
                usuario = request.user
                instanciaSkin = Skin.objects.get(nombreSkin = skin)
                usuario.skinUser = instanciaSkin
                usuario.save()
        return render(request, 'adminlte/index.html')


def simple_upload(request):
    if request.method == 'POST':
        usuario = request.user
        usuario.avatar = request.FILES.get('file')
        
        usuario.save()
    return render(request, 'adminlte/index.html')
                
#Api
from django.http import JsonResponse
from rest_framework import viewsets

from rest_framework.filters import OrderingFilter
from django_filters.rest_framework import DjangoFilterBackend

from .serializers import GrupoSerializer
from .serializers import UserSerializer
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
