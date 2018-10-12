from rest_framework import serializers
from .models import Grupo, UserManager, Suscripcion

class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = UserManager
        fields = ('username','email',)

class GrupoSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Grupo
        fields = ('idGrupo','NombreGrupo', 'Creador')


class SuscripcionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Suscripcion
        fields = '__all__'
        depth = 1