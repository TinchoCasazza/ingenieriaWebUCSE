from django.shortcuts import render

# Create your views here.

def login_prueba(request):
    return render(request, 'index_login.html')