from rest_framework import serializers
from .models import Grupo, UserManager


class GrupoSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Grupo
        fields = ('idGrupo','NombreGrupo')

