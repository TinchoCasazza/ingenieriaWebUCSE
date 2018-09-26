"""example_project URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.10/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf import settings
from django.conf.urls import url, include
from django.contrib import admin
from django.views.generic.base import TemplateView
from ingenieria_web.social import views as social_views
from ingenieria_web.search import views as search_views
from django.contrib.auth.views import LoginView, login_required

urlpatterns = [

    # Acount
    url(r'^login/$', social_views.login, name="login_aux_url"),
    url(r'^logout/$', social_views.logout, name="logout_url"),
    url(r'^register/$', social_views.register, name="register_url"),
    
    # Inicio
    url(r'^$', social_views.inicio, name="inicio_url"),
    url(r'^inicio/$', social_views.inicio, name="inicio_url"),
    url(r'^admin/', admin.site.urls),

    #Publicaciones
    url(r'^publicar/$', social_views.publicar, name="publicar_url"),

    #Grupos
    url(r'^grupos/$', social_views.grupos, name="grupos_url"),   

    #Busqueda
    url(r'^busqueda/$', search_views.search, name="search_url"),  
]

if settings.DEBUG:
    import debug_toolbar
    urlpatterns += [
        url(r'^__debug__/', include(debug_toolbar.urls)),
    ]
