from django.shortcuts import render
from ingenieria_web.search.documents import GrupoDocument
# Create your views here.

def search(request):

    q = request.GET.get('q')

    if q:
        grupos = GrupoDocument.search().query("match", NombreGrupo=q)
    else:
        grupos = ''

    return render(request, 'adminlte/search.html', {'grupos':grupos})