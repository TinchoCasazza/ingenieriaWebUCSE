from django.contrib import admin
from django_summernote.admin import SummernoteModelAdmin
<<<<<<< HEAD
from .models import Evento, Perfil,Grupo, UserGrupos, Publicacion, Comentario,Carrera,Skin, UserManager,  Suscripcion, DenunciaUsuarios, DenunciaGrupos, DenunciaUser
class PublicacionAdmin(SummernoteModelAdmin):  # instead of ModelAdmin
    summernote_fields = '__all__'
# Register your models here.
admin.register(Evento, Grupo, UserGrupos,Perfil, Comentario,Carrera,Skin, UserManager, Suscripcion, DenunciaUsuarios, DenunciaGrupos, DenunciaUser)(admin.ModelAdmin)
=======
from .models import Evento, Perfil,Grupo, UserGrupos,SuspensionUsuario, Publicacion, Comentario,Carrera,Skin, UserManager,  Suscripcion, DenunciaUsuarios, DenunciaGrupos
class PublicacionAdmin(SummernoteModelAdmin):  # instead of ModelAdmin
    summernote_fields = '__all__'
# Register your models here.
admin.register(Evento, Grupo, UserGrupos,Perfil,SuspensionUsuario, Comentario,Carrera,Skin, UserManager, Suscripcion, DenunciaUsuarios, DenunciaGrupos)(admin.ModelAdmin)
>>>>>>> 7c92da6fa85d09dd1f1336e6321924795c4878c6

admin.site.register(Publicacion,PublicacionAdmin)


