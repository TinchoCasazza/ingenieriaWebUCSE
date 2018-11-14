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
from django.contrib.auth import views as auth_views
from django.contrib.auth.views import LoginView, login_required
from rest_framework import routers
from rest_framework.authtoken import views
router = routers.DefaultRouter()
router.register('grupos', social_views.GrupoViewSet)
router.register('usuarios', social_views.UserViewSet)
router.register('suscripcion', social_views.SuscripcionViewSet)
router.register('publicacion', social_views.PublicacionViewSet)
router.register('tokens', social_views.TokensViewSet)
router.register('comentarios', social_views.ComentarioViewSet)
router.register('usergrupos', social_views.UserGruposViewSet)

urlpatterns = [

    # Acount
    url(r'^login/$', social_views.login, name="login_aux_url"),
    url(r'^logout/$', social_views.logout, name="logout_url"),
    url(r'^signup/$', social_views.signup, name='signup'),
    url(r'^activate/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',
        social_views.activate, name='activate'),
    
    # Inicio
    url(r'^$', social_views.inicio, name="inicio_url"),
    url(r'^inicio/$', social_views.inicio, name="inicio_url"),
    url(r'^admin/', admin.site.urls),

    #Publicaciones
    url(r'^publicar/$', login_required(social_views.publicar), name="publicar_url"),
    url(r'^publicar/borrar/$', login_required(social_views.borrarPublicacion), name="borrarPublicacion_url"),
    url(r'^publicar/guardar/$', login_required(social_views.guardarPublicacion), name="guardarPublicacion_url"),
    url(r'^publicar/comentar/$', login_required(social_views.comentarPublicacion), name="comentarPublicacion_url"),
    url(r'^publicar/denunciar/$', login_required(social_views.denunciarPublicacion), name="denunciarPublicacion_url"),
    url(r'^publicacion/(?P<pk>\d+)/$', login_required(social_views.publicaciones), name="publicacion_url_with_pk"),
    url(r'^publicacion/(?P<pk>\d+)/destacar$', login_required(social_views.destacarPublicacion), name="destacar_publicacion_pk"),
    url(r'^publicacion/(?P<pk>\d+)/eliminar$', login_required(social_views.eliminarPublicacion), name="eliminar_publicacion_pk"),
    #Grupos
    url(r'^grupos/$', login_required(social_views.grupos), name="grupos_url"),   
    url(r'^grupos/(?P<pk>\d+)$', login_required(social_views.grupos), name="grupos_url_with_pk"),
    url(r'^grupos/crear_grupo/$', login_required(social_views.crear_grupo), name="grupos_url_create"),     
    url(r'^grupos/suscribirse/$', login_required(social_views.suscribirUsuario), name="grupos_url_suscripcion"),     
    url(r'^grupos/tema/$', login_required(social_views.grupos_tema), name="grupos_url_tema"),     
    url(r'^grupos/(?P<pk>\d+)/nuevaPublicacion$', login_required(social_views.grupo_publicacion), name="nueva_publicacion_with_pk"),
    url(r'^grupos/agregar_miembro/$', login_required(social_views.agregar_miembro_grupo), name="grupos_agregar_miembro"),
    url(r'^grupos/(?P<pk>\d+)/admin$', login_required(social_views.administrarGrupo), name="admin_grupo"),
    url(r'^grupos/(?P<pk>\d+)/admin/privacidad$', login_required(social_views.cambiarPrivacidadGrupo), name="cambiar_privacidad"),
    url(r'^grupos/(?P<pkGrupo>\d+)/admin/(?P<pkUser>\d+)/$', login_required(social_views.banearUsuario), name="banear_Usuario"),
    url(r'^grupos/(?P<pkGrupo>\d+)/eliminar$', login_required(social_views.borrarGrupo), name="borrar_Grupo"),
    url(r'^grupos/denunciar/$', login_required(social_views.denunciarGrupos), name="denunciar_grupo_url"),
    url(r'^grupos/(?P<pk>\d+)/salirgrupo$', login_required(social_views.salirGrupo), name="salir_grupo"),   

    #Denuncias
    url(r'^denuncias/$', login_required(social_views.denuncias), name="denuncias_url"),
    url(r'^denuncias/(?P<pk>\d+)/eliminar$', login_required(social_views.moderarDenuncia), name="moderar_denuncia_pk"),
    url(r'^denuncias/(?P<pk>\d+)/usuario/eliminar$', login_required(social_views.moderarDenunciaUser), name="moderar_denuncia_user_pk"),
    url(r'^denuncias/(?P<pk>\d+)/grupo/eliminar$', login_required(social_views.moderarDenunciaGrupo), name="moderar_denuncia_grupo_pk"),

    #Eventos
    url(r'^grupos/(?P<pk>\d+)/nuevoEvento$', login_required(social_views.CrearEvento), name="nuevo_evento_with_pk"),

    url(r'^summernote/', include('django_summernote.urls')),

    #Busqueda
    url(r'^busqueda/$', search_views.search, name="search_url"),  

    #Perfil
    url(r'^perfil/denunciar/$', login_required(social_views.denunciarUser), name="denunciar_user_url"),
    url(r'^perfil/(?P<pk>[\w\-]+)/$', social_views.perfil, name="perfil_url_pk"),  
    #Skin
    url(r'^cambiarSkin/$', social_views.cambiarSkin, name="cambiarSkin_url"),  

    #FotoPerfil
    url(r'^fotoPerfil/$', social_views.cambiarFotoPerfil, name="fotoPerfil_url"),  
    
    #Api
    url(r'ejemplo_api_v1/$', social_views.api_v1),
    url(r'api_v1/cantidad_grupos/$', social_views.api_cantidad_grupos),
    url(r'api_v1/', include(router.urls)),
    url(r'ApiToken_auth/$', views.obtain_auth_token, name="ApiToken_auth"),

    #Recuperar Contraseña
    url(r'^password_reset/$', auth_views.PasswordResetView.as_view(template_name ='adminlte/registration/password_reset_form.html'), name='password_reset'),
    url(r'^password_reset/done/$', auth_views.PasswordResetDoneView.as_view(template_name ='adminlte/registration/password_reset_done.html'), name='password_reset_done'),
    url(r'^reset/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',
        auth_views.PasswordResetConfirmView.as_view(template_name ='adminlte/registration/password_reset_confirm.html'), 
            name='password_reset_confirm'),
    url(r'^reset/done/$', auth_views.PasswordResetCompleteView.as_view(template_name ='adminlte/login.html'), name='password_reset_complete'),

]

if settings.DEBUG:
    import debug_toolbar
    urlpatterns += [
        url(r'^__debug__/', include(debug_toolbar.urls)),
    ]


from django.conf.urls.static import static
 
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)