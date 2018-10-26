from django.shortcuts import render
from ingenieria_web.search.documents import GrupoDocument
from ingenieria_web.social.forms import NuevoGrupo
from ingenieria_web.social.models import Suscripcion
# Create your views here.

def search(request):
    q = request.GET.get('q')
    formNuevoGrupo = NuevoGrupo()
    listaSuscripciones = Suscripcion.objects.all().order_by('-fecha_peticion')
    if q:
        grupos = GrupoDocument.search().query("match", NombreGrupo=q)
    else:
        grupos = ''

    return render(request, 'adminlte/search.html', {'grupos':grupos, 'formNuevoGrupo': formNuevoGrupo,'listaSuscripciones':listaSuscripciones})