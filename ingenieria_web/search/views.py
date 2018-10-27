from django.shortcuts import render
from ingenieria_web.search.documents import GrupoDocument
from ingenieria_web.social.models import UserGrupos, Grupo
# Create your views here.

def search(request):
    q = request.GET.get('q')

    if q:
        grupos = GrupoDocument.search().query("match", NombreGrupo=q)
    else:
        grupos = ''

    misGrupos = UserGrupos.objects.filter(idUser = request.user).values_list('idGrupoUsuario', flat=True)
    
    print(misGrupos)

    
    return render(request, 'adminlte/search.html', {'grupos':grupos, 'misGrupos':misGrupos})