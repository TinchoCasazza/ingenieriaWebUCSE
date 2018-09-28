from django.contrib import admin
from .models import PrivacidadGrupo, Grupo, UserGrupos, Publicacion, EstadoPublicacion
# Register your models here.
admin.register(PrivacidadGrupo, Grupo, UserGrupos, Publicacion, EstadoPublicacion)(admin.ModelAdmin)