from django.contrib import admin
from django_summernote.admin import SummernoteModelAdmin
from .models import PrivacidadGrupo, Evento, Grupo, UserGrupos, Publicacion, Comentario,Carrera,Skin, UserManager,  Suscripcion, DenunciaUsuarios
class PublicacionAdmin(SummernoteModelAdmin):  # instead of ModelAdmin
    summernote_fields = '__all__'
# Register your models here.
admin.register(Evento, PrivacidadGrupo, Grupo, UserGrupos, Comentario,Carrera,Skin, UserManager, Suscripcion, DenunciaUsuarios)(admin.ModelAdmin)

admin.site.register(Publicacion,PublicacionAdmin)


