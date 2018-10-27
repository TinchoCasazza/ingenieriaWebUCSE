from django.contrib import admin
from django_summernote.admin import SummernoteModelAdmin
from .models import PrivacidadGrupo, Grupo, UserGrupos, Publicacion, Comentario,Carrera,Skin, UserManager, Permisos, Suscripcion, DenunciaUsuarios
class PublicacionAdmin(SummernoteModelAdmin):  # instead of ModelAdmin
    summernote_fields = '__all__'
# Register your models here.
admin.register(PrivacidadGrupo, Grupo, UserGrupos, Comentario,Carrera,Skin, UserManager, Permisos, Suscripcion, DenunciaUsuarios)(admin.ModelAdmin)

admin.site.register(Publicacion,PublicacionAdmin)


