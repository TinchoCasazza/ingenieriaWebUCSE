from django.contrib import admin
from .models import PrivacidadGrupo, Grupo, UserGrupos, Publicacion, Comentario,Carrera,Skin, UserManager, Permisos
# Register your models here.
admin.register(PrivacidadGrupo, Grupo, UserGrupos, Publicacion, Comentario,Carrera,Skin, UserManager, Permisos)(admin.ModelAdmin)