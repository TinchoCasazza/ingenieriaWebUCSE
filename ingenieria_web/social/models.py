from django.db import models
from django.utils import timezone
from django.contrib.auth.models import AbstractUser
import datetime

from django.db.models.signals import post_save
from django.dispatch import receiver
from django.conf import settings
from ingenieria_web.social.choices import *
# Create your models here.


class Carrera(models.Model):
    idCarrera = models.AutoField(primary_key=True)
    NombreCarrera = models.CharField(blank = False, max_length=40)

    def __str__(self):
        return (self.NombreCarrera)

class Skin(models.Model):
    idSkin = models.AutoField(primary_key= True)
    nombreSkin = models.CharField(blank = False, max_length=40)

    def __str__(self):
        return (self.nombreSkin)
    

class UserManager(AbstractUser):
    carrera = models.ForeignKey(Carrera, on_delete=models.CASCADE, null=True)
    skinUser = models.ForeignKey(Skin, on_delete=models.CASCADE, null=True)
    avatar = models.CharField(blank = True, null=True, max_length=40)


class Perfil(models.Model):
    idPerfil = models.AutoField(primary_key=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    nombreCompleto = models.CharField(blank = True, null=True, max_length=50, default="Agregar Nombre")
    localizacion = models.CharField(blank = True, null=True, max_length=50, default="Agregar Ubicacion")
    carrera = models.CharField(blank = True, null=True, max_length=40, default="Agregar Carrera")
    universidad = models.CharField(blank = True, null=True, max_length=100, default="Agregar Universidad")

class SuspensionUsuario(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    motivo = models.CharField(blank = True, null=True, max_length=100)
    fechaSuspension = models.DateField(default = datetime.date.today, editable = False)
    duracion = models.IntegerField(blank = True, null=True)
class Grupo(models.Model):
    idGrupo = models.AutoField(primary_key=True)
    NombreGrupo = models.CharField(blank= False, max_length=50)
    Creador = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    NivelAcceso = models.IntegerField(choices=PRIVACITY_CHOICES, default=1)
    FechaCreacionG = models.DateField(("Fecha Creacion"), default = datetime.date.today, editable = False)
    FechaBajaG = models.DateField(default= None, null = True, editable = False)
    FechaModiG = models.DateField(default = None, null = True, editable = False)

    def __str__(self):
        return (self.NombreGrupo)



class UserGrupos(models.Model):
    idUser = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    idGrupoUsuario = models.ForeignKey(Grupo, on_delete=models.CASCADE)
    Rango = models.IntegerField(choices=RANK_CHOICES, default=1)

  



class Publicacion(models.Model):
    idPublicacion = models.AutoField(primary_key= True)
    idUserPublico = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    idGrupoPu = models.ForeignKey(Grupo, on_delete=models.CASCADE, null = True)
    Destacar = models.IntegerField(choices=RELEVANCE_CHOICES, default=1)
    Estado = models.IntegerField(choices=STATUS_CHOICES, default=1)
    Titulo = models.CharField(blank=False, max_length = 30)
    Contenido = models.TextField(blank=False)
    FechaPublicacion = models.DateField(("Date"), auto_now=True, editable = False)
    FechaBajaPublicacion = models.DateField(default= None, editable = False,null = True)
    FechaModiPublicacion = models.DateField(default = None, editable = False, null = True)

    def __str__(self):
        return (self.Titulo)

class DenunciaUsuarios(models.Model):
    idUsuario =  models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    idPublicacion = models.ForeignKey(Publicacion, on_delete=models.CASCADE) 
    Contenido = models.TextField(blank=False, max_length = 150)

class DenunciaGrupos(models.Model):
    idUsuario =  models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    idGrupo = models.ForeignKey(Grupo, on_delete=models.CASCADE) 
    Contenido = models.TextField(blank=False, max_length = 150)

class DenunciaUser(models.Model):
    idUsuario =  models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='userDenuncia')
    idUsuarioDenunciado = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE,related_name='userDenunciado') 
    Contenido = models.TextField(blank=False, max_length = 150)


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
    Estado = models.IntegerField(choices=STATUS_CHOICES, default=1)

from django.utils.timezone import now
class Evento(models.Model):
    idEvento = models.AutoField(primary_key = True)
    idGrupoEvento = models.ForeignKey(Grupo, on_delete=models.CASCADE, null = True)
    NombreEvento = models.CharField(blank=False, max_length = 30)
    CreadorEvento = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='CreadorEvento')
    FechaEvento = models.DateTimeField(blank= False, default = now)
    Hora = models.TimeField(blank= False)
