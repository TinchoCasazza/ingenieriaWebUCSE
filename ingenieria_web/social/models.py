from django.db import models
from django.utils import timezone
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.models import User
import datetime
# Create your models here.


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
    Creador = models.ForeignKey(User, on_delete=models.CASCADE)
    NivelAcceso = models.ForeignKey(PrivacidadGrupo, on_delete=models.CASCADE)
    FechaCreacionG = models.DateField(("Fecha Creacion"), default = datetime.date.today)
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


class UserGrupos(models.Model):
    idUser = models.ForeignKey(User, on_delete=models.CASCADE)
    idGrupoUsuario = models.ForeignKey(Grupo, on_delete=models.CASCADE)
    Permisos = models.ForeignKey(Permisos, on_delete=models.CASCADE)


class Publicacion(models.Model):
    idPublicacion = models.AutoField(primary_key= True)
    idUserPublico = models.ForeignKey(User, on_delete=models.CASCADE)
    idGrupoPu = models.ForeignKey(Grupo, on_delete=models.CASCADE, null = True)
    Destacar = models.BooleanField(default = False)
    Titulo = models.CharField(blank=False, max_length = 30)
    Contenido = models.TextField(blank=False)
    FechaPublicacion = models.DateField(("Date"), auto_now=True)
    FechaBajaPublicacion = models.DateField(default= None, editable = False,null = True)
    FechaModiPublicacion = models.DateField(default = None, editable = False, null = True)


class Comentario(models.Model):
    idComentario = models.AutoField(primary_key = True)
    idUserComento = models.ForeignKey(User, on_delete=models.CASCADE)
    idPublicacionC = models.ForeignKey(Publicacion, on_delete=models.CASCADE)
    ContenidoComentario = models.TextField(null = True)
    FechaComentario = models.DateField(("Date"), auto_now=True)
    FechaModiComentario = models.DateField(default = None, editable = False, null = True)
    FechaBajaComentario = models.DateField(default = None, editable = False, null = True)




