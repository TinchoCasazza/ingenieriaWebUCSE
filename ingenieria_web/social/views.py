from django.shortcuts import render
from django.contrib import messages
from django.http import HttpResponseRedirect
from django.template import context
from .models import Publicacion, Grupo, Comentario

from django.http import HttpResponse
from django.shortcuts import render, redirect
from .forms import SignupForm
from django.contrib.sites.shortcuts import get_current_site
from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.template.loader import render_to_string
from .tokens import account_activation_token
from django.contrib.auth.models import User
from django.core.mail import EmailMessage
from django.contrib.auth.forms import UserCreationForm 
from django.contrib.auth.models import (
    BaseUserManager, AbstractBaseUser
)
from .forms import NuevoGrupo

from django.contrib.auth import authenticate, login
from django.contrib.auth import logout as django_logout
from django.contrib.auth import login as auth_login
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


def grupos(request):
        lista_Grupos = Grupo.objects.all().order_by('NombreGrupo')
        return render(request, 'adminlte/grupos.html', {'lista_grupos' : lista_Grupos})

