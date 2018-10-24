from django.db import models
from django.utils import timezone
from django.contrib.auth.models import AbstractUser
import datetime

from django.db.models.signals import post_save
from django.dispatch import receiver
from django.conf import settings
# Create your models here.


class Carrera(models.Model):
    idCarrera = models.AutoField(primary_key=True)
    NombreCarrera = models.CharField(blank = False, max_length=40)

class Skin(models.Model):
    idSkin = models.AutoField(primary_key= True)
    nombreSkin = models.CharField(blank = False, max_length=40)

    def __str__(self):
        return (self.nombreSkin)
    

class UserManager(AbstractUser):
    carrera = models.ForeignKey(Carrera, on_delete=models.CASCADE, null=True)
    skinUser = models.ForeignKey(Skin, on_delete=models.CASCADE, null=True)
    avatar = models.CharField(blank = True, null=True, max_length=40)



class CategoriaUsuario(models.Model):
    idCategoriaU = models.AutoField(primary_key=True)
    NombreCategoriaU = models.CharField(blank=False, max_length=50)

    def __str__(self):
        return (self.NombreCategoriaU)

class PrivacidadGrupo(models.Model):
    idPrivacidadG = models.AutoField(primary_key=True)
    Privacidad = models.CharField(blank=False, max_length=50)

    def __str__(self):
        return (self.Privacidad)

class Grupo(models.Model):
    idGrupo = models.AutoField(primary_key=True)
    NombreGrupo = models.CharField(blank= False, max_length=50)
    Creador = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    NivelAcceso = models.ForeignKey(PrivacidadGrupo, on_delete=models.CASCADE)
    FechaCreacionG = models.DateField(("Fecha Creacion"), default = datetime.date.today, editable = False)
    FechaBajaG = models.DateField(default= None, null = True, editable = False)
    FechaModiG = models.DateField(default = None, null = True, editable = False)

    def __str__(self):
        return (self.NombreGrupo)


class Permisos(models.Model):
    idPermisos = models.AutoField(primary_key = True)
    NombrePerm = models.CharField(max_length = 30, blank = False)
    EditarComentarios = models.BooleanField(default = False)
    EliminarComentarios = models.BooleanField(default = False)
    EditarPublicacion = models.BooleanField(default = False)
    EliminarPublicacion = models.BooleanField(default = False)
    EditarGrupo = models.BooleanField(default = False)
    EliminarGrupo = models.BooleanField(default = False)

    def __str__(self):
        return (self.NombrePerm)


class UserGrupos(models.Model):
    idUser = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    idGrupoUsuario = models.ForeignKey(Grupo, on_delete=models.CASCADE)
    Permisos = models.ForeignKey(Permisos, on_delete=models.CASCADE)




class Publicacion(models.Model):
    idPublicacion = models.AutoField(primary_key= True)
    idUserPublico = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    idGrupoPu = models.ForeignKey(Grupo, on_delete=models.CASCADE, null = True)
    Destacar = models.BooleanField(default = False)
    Publicado = models.BooleanField(default = False, null=True)
    Borrador = models.BooleanField(default = False, null=True)
    Eliminado = models.BooleanField(default = False, null=True)
    Titulo = models.CharField(blank=False, max_length = 30)
    Contenido = models.TextField(blank=False)
    FechaPublicacion = models.DateField(("Date"), auto_now=True, editable = False)
    FechaBajaPublicacion = models.DateField(default= None, editable = False,null = True)
    FechaModiPublicacion = models.DateField(default = None, editable = False, null = True)

class DenunciaUsuarios(models.Model):
    idUsuario =  models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    idPublicacion = models.ForeignKey(Publicacion, on_delete=models.CASCADE) 

class Comentario(models.Model):
    idComentario = models.AutoField(primary_key = True)
    idUserComento = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    idPublicacionC = models.ForeignKey(Publicacion, on_delete=models.CASCADE)
    ContenidoComentario = models.TextField(null = True)
    FechaComentario = models.DateField(("Date"), auto_now=True)
    FechaModiComentario = models.DateField(default = None, editable = False, null = True)
    FechaBajaComentario = models.DateField(default = None, editable = False, null = True)

class Suscripcion(models.Model):
    idSuscripcion = models.AutoField(primary_key = True)
    emisor = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='emisor')
    receptor = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='receptor')
    idGrupoSuscribio = models.ForeignKey(Grupo, on_delete=models.CASCADE, null = True)
    fecha_peticion = models.DateField(auto_now=True)
