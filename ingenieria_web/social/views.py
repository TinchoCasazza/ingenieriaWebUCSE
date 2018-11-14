from django.shortcuts import render
from django.contrib import messages
from django.http import HttpResponseRedirect
from django.template import context
from .models import Publicacion, Grupo, Comentario, Skin, Perfil, UserGrupos, Suscripcion, DenunciaUsuarios, DenunciaGrupos, DenunciaUser
from rest_framework.authtoken.models import Token
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
    listaPublicaciones = Publicacion.objects.filter(Estado = 4).order_by('-FechaPublicacion')
    listaGrupos = Grupo.objects.all().order_by('NombreGrupo')
    listaComentarios = Comentario.objects.all()
    listaSuscripciones = Suscripcion.objects.filter(Estado = 1).order_by('-fecha_peticion')
    formNuevoGrupo = NuevoGrupo()
    formNuevaPublicacion = PublicacionForm()
    return render(request, 'adminlte/index.html',{'listaPublicaciones' : listaPublicaciones ,'listaGrupos': listaGrupos, 'formNuevoGrupo': formNuevoGrupo, 'listaComentarios': listaComentarios, 'listaSuscripciones': listaSuscripciones,'formNuevaPublicacion':formNuevaPublicacion})


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
                                token, _ = Token.objects.get_or_create(user=user)
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
                form = PublicacionForm(request.POST)
                
                if form.is_valid():
                        
                        publicacion = form.save(commit=False)
                        publicacion.Estado = 4
                        publicacion.idUserPublico = request.user
                        publicacion.save()
                return HttpResponseRedirect('/inicio/')
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

                data = {
                   'mensaje' : "Denuncia Exitosa"
                } 
        return JsonResponse(data)
                
def denuncias(request):
        DenunciasPublicaciones = DenunciaUsuarios.objects.all()
        DenunciasGrupos = DenunciaGrupos.objects.all()

        return render(request, 'adminlte/denuncias.html', {'DenunciasPublicaciones' : DenunciasPublicaciones, 'DenunciasGrupos': DenunciasGrupos})

def moderarDenuncia(request, pk=None):
        if pk:
                publicacion = Publicacion()
                publicacion = Publicacion.objects.get(idPublicacion = pk)
                publicacion.Estado = 2 
                publicacion.save()

                DenunciaUsuarios.objects.filter(idPublicacion = pk).delete()
                
        
        DenunciasPublicaciones = DenunciaUsuarios.objects.all()
        DenunciasGrupos = DenunciaGrupos.objects.all()
        return render(request, 'adminlte/denuncias.html', {'DenunciasPublicaciones' : DenunciasPublicaciones, 'DenunciasGrupos': DenunciasGrupos})

def moderarDenunciaGrupo(request, pk=None):
        if pk:
                grupo = Grupo()
                grupo = Grupo.objects.get(idGrupo= pk)
                grupo.Estado = 2 
                grupo.save()

                DenunciaGrupos.objects.filter(idGrupo = pk).delete()
                
        
        DenunciasPublicaciones = DenunciaUsuarios.objects.all()
        DenunciasGrupos = DenunciaGrupos.objects.all()
        return render(request, 'adminlte/denuncias.html', {'DenunciasPublicaciones' : DenunciasPublicaciones, 'DenunciasGrupos': DenunciasGrupos})

from .forms import EventoForm
from .models import Evento
def ValidarAcceso(request, pkGrupo):
        if UserGrupos.objects.filter(idUser = request.user, idGrupoUsuario = pkGrupo).exists():
                return True
        else:
                return False        

def grupos(request, pk=None):
        listaSuscripciones = Suscripcion.objects.filter(Estado = 1).order_by('-fecha_peticion')
        formNuevoGrupo = NuevoGrupo()
        if pk:
                grupo = Grupo.objects.get(idGrupo=pk)
                if (grupo.NivelAcceso == 2 and ValidarAcceso(request, grupo.idGrupo) == True) or grupo.NivelAcceso == 1:
                        miembros_grupos = []
                        for miembro_grupo in UserGrupos.objects.filter(idGrupoUsuario = grupo):
                                miembros_grupos.append(miembro_grupo.idUser)
                        User = get_user_model()
                        miembros = User.objects.filter(username__in = miembros_grupos)
                        valido = False
                        if request.user in miembros:
                                valido = True
                                
                        publicaciones = Publicacion.objects.filter(idGrupoPu = pk, Estado = 1).order_by('-Destacar')
                        nuevoEventoForm = EventoForm()
                        eventos = Evento.objects.filter(idGrupoEvento = pk)
                        miembroGrupo = UserGrupos.objects.get(idUser = request.user, idGrupoUsuario = pk)
                        return render(request, 'adminlte/grupo_tema.html', {'grupo' : grupo, 'miembros' : miembros, 'publicaciones':publicaciones,'listaSuscripciones': listaSuscripciones, 'formNuevoGrupo': formNuevoGrupo, 'valido':valido, 'nuevoEventoForm':nuevoEventoForm, 'eventos': eventos, 'miembroGrupo':miembroGrupo })
        lista_gruposuser = UserGrupos.objects.all().filter(idUser=request.user)
        lista_Grupos = Grupo.objects.all().order_by('NombreGrupo')
        lista_grupos = []
        for grupo in lista_Grupos:
            for grupouser in lista_gruposuser:
                if grupo == grupouser.idGrupoUsuario:
                    lista_grupos.append(grupo)
        publicaciones = Publicacion.objects.all()
        return render(request, 'adminlte/grupos.html', {'lista_grupos' : lista_grupos,'publicaciones':publicaciones,'listaSuscripciones': listaSuscripciones, 'formNuevoGrupo': formNuevoGrupo})
from .forms import ComentarioForm
def publicaciones(request, pk=None):
        publicacion = Publicacion.objects.get(idPublicacion = pk)
        comentarios = Comentario.objects.filter(idPublicacionC = publicacion.idPublicacion)
        grupo = Grupo.objects.get(idGrupo = publicacion.idGrupoPu.idGrupo)
        if (grupo.NivelAcceso == 2 and ValidarAcceso(request, grupo.idGrupo) == True) or grupo.NivelAcceso == 1:
                if request.method == 'POST':
                        form = ComentarioForm(request.POST)
                        if form.is_valid():
                                comentario = form.save(commit=False)
                                comentario.idUserComento = request.user
                                comentario.idPublicacionC = publicacion
                                comentario.save()
                FormComentario = ComentarioForm()
                listaSuscripciones = Suscripcion.objects.filter(Estado = 1).order_by('-fecha_peticion')
                formNuevoGrupo = NuevoGrupo()        
                return render(request, 'adminlte/publicacion.html', {'listaSuscripciones':listaSuscripciones,'formNuevoGrupo':formNuevoGrupo,'publicacion': publicacion, 'comentarios':comentarios, 'FormComentario': FormComentario} )
        else:
                return render(request, 'adminlte/errores/errorPrivado.html')
from django.urls import reverse
def grupo_publicacion(request, pk=None):
        grupo = Grupo.objects.filter(idGrupo = pk)[0]
        if request.method == 'POST':
                form = PublicacionForm(request.POST)
                if form.is_valid():
                        publicacion = form.save(commit=False)
                        gruposuser = UserGrupos.objects.filter(idUser = request.user)
                        if pk in gruposuser:
                                return  render(request,'adminlte/errores/errorPublicar.html')
                        publicacion.idUserPublico = request.user
                        publicacion.idGrupoPu = Grupo.objects.filter(idGrupo = pk)[0]
                        publicacion.save()
                return HttpResponseRedirect('/grupos/'+pk)
        if request.method == 'GET':
                formNuevaPublicacion = PublicacionForm()
                listaSuscripciones = Suscripcion.objects.filter(Estado = 1).order_by('-fecha_peticion')
                formNuevoGrupo = NuevoGrupo()
                return render(request, 'adminlte/publicacion_grupo.html', {'listaSuscripciones':listaSuscripciones,'formNuevoGrupo':formNuevoGrupo,'formNuevaPublicacion':formNuevaPublicacion,'grupo':grupo})

def crear_grupo(request):
        if request.method == 'POST':
                nombreGrupo = request.POST.get('nombreGrupo')
                nivelAcceso = request.POST.get('nivelAcceso')
                if nivelAcceso == 'Privado':
                        nivelAcceso = 2
                else:
                        nivelAcceso = 1
                grupo = Grupo()
                usergrupo = UserGrupos()
                grupo.NombreGrupo = nombreGrupo

                grupo.NivelAcceso = nivelAcceso
                grupo.Creador = request.user
                grupo.save()
               
                usergrupo.idGrupoUsuario = grupo
                usergrupo.idUser = grupo.Creador
                usergrupo.Rango = 3
               
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
                
                
                
                userGrupos.Rango = 1
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
                perfil = Perfil.objects.get(user = user)
                listaPublicaciones = Publicacion.objects.filter( idUserPublico = user, Estado=4).order_by('-FechaPublicacion')[:5]
        return render(request, 'adminlte/perfil.html',{'listaPublicaciones' : listaPublicaciones, 'user': user, 'perfil':perfil})

def denunciarUser(request):
        if request.method == 'POST':
                pkUser = request.POST.get('id')
                contenido = request.POST.get('contenido')
                denunciaUser = DenunciaUser()
                cantidad = DenunciaUser.objects.filter(idUsuario = request.user, idUsuarioDenunciado = pkUser).count()
                
                if cantidad < 1:
                        user = User.objects.get(id =pkUser)
                
                        denunciaUser = DenunciaUser()
                        denunciaUser.idUsuario = request.user
                        denunciaUser.idUsuarioDenunciado = user
                        denunciaUser.Contenido = contenido
                        denunciaUser.save()

                data = {
                   'mensaje' : "Denuncia Exitosa"
                } 
        return JsonResponse(data)

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

def CrearEvento(request, pk=None):
        if pk:
                form = EventoForm(request.POST)
                if form.is_valid():
                        evento = form.save(commit=False)
                        gruposuser = UserGrupos.objects.filter(idUser = request.user)

                        if pk in gruposuser:
                                return  render(request,'adminlte/errores/errorPublicar.html')
                        evento.CreadorEvento = request.user
                        evento.idGrupoEvento = Grupo.objects.filter(idGrupo = pk)[0]
                        evento.save()
                return HttpResponseRedirect('/grupos/'+pk)

def destacarPublicacion(request, pk=None):
        if pk:
                publicacion = Publicacion.objects.get(idPublicacion=pk)
                grupo = publicacion.idGrupoPu
                
                miembros_grupos = []
                for miembro_grupo in UserGrupos.objects.filter(idGrupoUsuario = grupo):
                   miembros_grupos.append(miembro_grupo.idUser)
                User = get_user_model()
                miembros = User.objects.filter(username__in = miembros_grupos)
                valido = False
                for miembro in miembros:
                        if request.user == miembro:
                                aux = UserGrupos.objects.filter(idUser=miembro,idGrupoUsuario=grupo)[0]
                                if aux.Rango > 1:
                                        valido = True
                if valido == True:
                        if publicacion.Destacar == 2:
                                publicacion.Destacar = 1
                        else:
                                publicacion.Destacar = 2
                        publicacion.save()
                pk_grupo = str(grupo.idGrupo)
                return HttpResponseRedirect('/grupos/'+pk_grupo)


def eliminarPublicacion(request, pk=None):
        if pk:
                publicacion = Publicacion.objects.get(idPublicacion=pk)
                grupo = publicacion.idGrupoPu
                
                miembros_grupos = []
                for miembro_grupo in UserGrupos.objects.filter(idGrupoUsuario = grupo):
                   miembros_grupos.append(miembro_grupo.idUser)
                User = get_user_model()
                miembros = User.objects.filter(username__in = miembros_grupos)
                valido = False
                for miembro in miembros:
                        if request.user == miembro:
                                aux = UserGrupos.objects.filter(idUser=miembro,idGrupoUsuario=grupo)[0]
                                if aux.Rango > 1:
                                        valido = True
                if valido == True:
                        publicacion.Estado = 2
                        publicacion.save()
                pk_grupo = str(grupo.idGrupo)
                return HttpResponseRedirect('/grupos/'+pk_grupo)

from .forms import AdminGrupoForm, PrivacidadGrupoForm        
def administrarGrupo(request, pk=None):
        grupo = Grupo.objects.get(idGrupo = pk)
        miembrosGrupos = UserGrupos.objects.filter(idGrupoUsuario = pk)
        if request.method == "GET":
                formPrivacidadGrupo = PrivacidadGrupoForm()
                formAdministrarGrupo = AdminGrupoForm()
                miembros_grupos = []
                for miembro_grupo in UserGrupos.objects.filter(idGrupoUsuario = pk):
                   miembros_grupos.append(miembro_grupo.idUser)
                User = get_user_model()
                miembros = User.objects.filter(username__in = miembros_grupos)
                formAdministrarGrupo.fields['idUser'].queryset = miembros
                miembro = UserGrupos.objects.get(idUser=request.user,idGrupoUsuario=pk)
                if miembro.Rango == 3:
                        return render(request, 'adminlte/adminGrupo.html', {'formAdministrarGrupo':formAdministrarGrupo, 'grupo':grupo, 'miembros':miembrosGrupos,'formPrivacidadGrupo':formPrivacidadGrupo})
                else:
                        return render(request, 'adminlte/errores/errorAdmin.html', { 'GrupoPk': pk})
        if request.method == "POST":
                form = AdminGrupoForm(request.POST)
                if form.is_valid():
                        miembro = UserGrupos.objects.get(idUser=form.cleaned_data.get('idUser'),idGrupoUsuario=pk)
                        miembro.Rango = form.cleaned_data.get('Rango')
                        miembro.save()
                formAdministrarGrupo = AdminGrupoForm()
                formPrivacidadGrupo = PrivacidadGrupoForm()
                return render(request, 'adminlte/adminGrupo.html', {'formAdministrarGrupo':formAdministrarGrupo, 'grupo': grupo, 'miembros': miembrosGrupos,'formPrivacidadGrupo':formPrivacidadGrupo})

def borrarGrupo(request,pkGrupo=None):
        if pkGrupo:
                Grupo.objects.filter(idGrupo=pkGrupo).delete()
        return HttpResponseRedirect("/grupos/")

def denunciarGrupos(request):
        if request.method == 'POST':
                pkGrupo = request.POST.get('id')
                contenido = request.POST.get('contenido')
                denunciaGrupo = DenunciaGrupos()
                cantidad = DenunciaGrupos.objects.filter(idUsuario = request.user, idGrupo = pkGrupo).count()
                if cantidad < 1:
                        grupo = Grupo()
                        grupo = Grupo.objects.get(idGrupo = pkGrupo)
                
                        denunciaGrupo = DenunciaGrupos()
                        denunciaGrupo.idUsuario = request.user
                        denunciaGrupo.idGrupo = grupo
                        denunciaGrupo.Contenido = contenido
                        denunciaGrupo.save()

                data = {
                   'mensaje' : "Denuncia Exitosa"
                } 
        return JsonResponse(data)

def banearUsuario(request, pkGrupo=None, pkUser=None):
        miembro = UserGrupos.objects.filter(idUser=request.user,idGrupoUsuario=pkGrupo)[0]
        if miembro.Rango == 3:
                UserGrupos.objects.filter(idUser=pkUser,idGrupoUsuario=pkGrupo).delete()
        return HttpResponseRedirect("/grupos/"+pkGrupo+"/admin")

def cambiarPrivacidadGrupo(request, pk=None):
        if pk:
                grupo = Grupo.objects.get(idGrupo = pk)
                form = PrivacidadGrupoForm(request.POST)
                if form.is_valid():
                        nivelAcceso = form.cleaned_data['NivelAcceso']
                        grupo.NivelAcceso = nivelAcceso
                        grupo.NivelAcceso = nivelAcceso
                        grupo.save()
        return HttpResponseRedirect("/grupos/"+pk+"/admin")

def salirGrupo(request, pk=None):
        if pk:
            miembro = UserGrupos.objects.get(idUser=request.user,idGrupoUsuario=pk)    
            grupo = Grupo.objects.get(idGrupo=pk)
            if grupo.Creador != request.user:
                    UserGrupos.objects.get(idUser=request.user,idGrupoUsuario=pk).delete()
                    Suscripcion.objects.get(emisor=request.user, idGrupoSuscribio = pk).delete()
                    return HttpResponseRedirect("/grupos/")
            else:
                    return HttpResponseRedirect("/grupos/"+pk)

#Api
from django.http import JsonResponse
from rest_framework import viewsets

from rest_framework.filters import OrderingFilter
from django_filters.rest_framework import DjangoFilterBackend

from .serializers import GrupoSerializer
from .serializers import UserSerializer
from .serializers import SuscripcionSerializer,PublicacionSerializer, TokenSerializer, ComentarioSerializer,UserGruposSerializer
from django.contrib.auth import get_user_model

def api_v1(request):
    return render(request, 'api_v1.html', {})

def api_cantidad_grupos(request):
    data = {
        'cantidad_grupos': Grupo.objects.count()
    }
    return JsonResponse(data)
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
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

class PublicacionViewSet(viewsets.ModelViewSet):
        queryset = Publicacion.objects.all()
        serializer_class = PublicacionSerializer
        filter_backends = (OrderingFilter, DjangoFilterBackend)
        permission_classes = (IsAuthenticated, )
        authentication_classes = (TokenAuthentication, )


class TokensViewSet(viewsets.ModelViewSet):
        queryset = Token.objects.all()
        serializer_class = TokenSerializer
        filter_backends = (OrderingFilter, DjangoFilterBackend)
        permission_classes = (IsAuthenticated, )
        authentication_classes = (TokenAuthentication, )

class ComentarioViewSet(viewsets.ModelViewSet):
        queryset = Comentario.objects.all()
        serializer_class = ComentarioSerializer
        filter_backends = (OrderingFilter, DjangoFilterBackend)
        permission_classes = (IsAuthenticated, )
        authentication_classes = (TokenAuthentication, )

       
class UserGruposViewSet(viewsets.ModelViewSet):
        queryset = UserGrupos.objects.all()
        serializer_class = UserGruposSerializer
        filter_backends = (OrderingFilter, DjangoFilterBackend)
        permission_classes = (IsAuthenticated, )
        authentication_classes = (TokenAuthentication, )


from django.db.models.signals import post_save
from django.dispatch import receiver
from rest_framework.authtoken.models import Token

@receiver(post_save, sender=get_user_model())
def create_auth_token(sender, instance=None, created=False, **kwargs):
    if created:
        Token.objects.create(user=instance)


User = get_user_model()


for user in User.objects.all():
    Token.objects.get_or_create(user=user)

for user in User.objects.all():
    Perfil.objects.get_or_create(user=user)

@receiver(post_save, sender=get_user_model())

def create_perfil(sender, instance=None, created=False, **kwargs):
    if created:
        Perfil.objects.create(user=instance)