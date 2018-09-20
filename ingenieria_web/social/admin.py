from django.contrib import admin
from .models import CategoriaGrupo, Grupo, UserGrupos, Publicacion
# Register your models here.
admin.register(CategoriaGrupo, Grupo, UserGrupos, Publicacion)(admin.ModelAdmin)