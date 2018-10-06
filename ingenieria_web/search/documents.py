from django_elasticsearch_dsl import DocType, Index
from ingenieria_web.social.models import Grupo

grupos = Index('grupos')

@grupos.doc_type
class GrupoDocument(DocType):
    class Meta:
        model = Grupo

        fields = [
            'idGrupo',
            'NombreGrupo',
        ]