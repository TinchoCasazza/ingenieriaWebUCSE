from rest_framework import serializers
from .models import Grupo, UserManager, Suscripcion, Publicacion, UserGrupos, Comentario
from rest_framework.authtoken.models import Token

class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = UserManager
        fields = ('id','username')

class GrupoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Grupo
        fields = ('idGrupo','NombreGrupo', 'Creador','NivelAcceso')


class SuscripcionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Suscripcion
        fields = '__all__'
        depth = 1

class PublicacionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Publicacion
        fields = '__all__'

class TokenSerializer(serializers.ModelSerializer):
    class Meta:
        model = Token
        fields = '__all__'

class UserGruposSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserGrupos
        fields = '__all__'

class ComentarioSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comentario
        fields = '__all__'
