from django.contrib import admin
from django_summernote.admin import SummernoteModelAdmin
from .models import Evento, Perfil,Grupo, UserGrupos,SuspensionUsuario, Publicacion, Comentario,Carrera,Skin, UserManager,  Suscripcion, DenunciaUsuarios, DenunciaGrupos
class PublicacionAdmin(SummernoteModelAdmin):  # instead of ModelAdmin
    summernote_fields = '__all__'
# Register your models here.
admin.register(Evento, Grupo, UserGrupos,Perfil,SuspensionUsuario, Comentario,Carrera,Skin, UserManager, Suscripcion, DenunciaUsuarios, DenunciaGrupos)(admin.ModelAdmin)

admin.site.register(Publicacion,PublicacionAdmin)


