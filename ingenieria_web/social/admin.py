from django.contrib import admin
from .models import PrivacidadGrupo, Grupo, UserGrupos, Publicacion, Carrera
# Register your models here.
admin.register(PrivacidadGrupo, Grupo, UserGrupos, Publicacion, Carrera)(admin.ModelAdmin)