from django.shortcuts import render
from django.contrib import messages
from django.http import HttpResponseRedirect
# Create your views here.

def inicio(request):
    return render(request, 'adminlte/index.html')

from django.contrib.auth import authenticate, login
from django.contrib.auth import logout as django_logout
from django.contrib.auth import login as auth_login
CRITICAL = 50
def login(request):
        if request.user.is_authenticated:
                return HttpResponseRedirect('inicio/')
        else:
                if request.method == 'POST':
                        username = request.POST.get('username')
                        password = request.POST.get('password')
                        user = authenticate(request, username=username, password=password)
                        if user is not None:
                                auth_login(request , user)
                                return render(request, 'adminlte/index.html', {})
                        else:
                                messages.set_level(request, messages.WARNING)
                                messages.add_message(request, CRITICAL, u'Usuario o Contrase\xf1a incorrectos.')
                                return render(request, 'adminlte/login.html' , {'error': messages} )
                else: 
                        return render(request, 'adminlte/login.html' ,{} )
       

def logout(request):
    django_logout(request)
    return  HttpResponseRedirect('/login/')

from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import (
    BaseUserManager, AbstractBaseUser
)
from django.contrib.auth.models import User


def register(request):
        if request.method == 'POST':
                username = request.POST.get('username')
                password = request.POST.get('password')

                user = User.objects.create_user(username= request.POST.get('username'),email=request.POST.get('email'),password=request.POST.get('password'))

                user.save()
                user = authenticate(request, username= username, password= password)
                if user is not None:
                        auth_login(request , user)
                        if request.user.is_authenticated:
                                return HttpResponseRedirect('/inicio/')
        else:
                form = UserCreationForm()
        return render(request, 'inicio.html', {'form': form})


