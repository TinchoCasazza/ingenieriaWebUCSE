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
                        username = request.POST['username']
                        password = request.POST['password']
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