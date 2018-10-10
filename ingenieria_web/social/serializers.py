from rest_framework import serializers
from .models import Grupo, UserManager

class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = UserManager
        fields = ('username','email',)

class GrupoSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Grupo
        fields = ('idGrupo','NombreGrupo', 'Creador')

