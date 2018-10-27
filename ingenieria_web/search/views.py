from django.shortcuts import render
from ingenieria_web.search.documents import GrupoDocument
<<<<<<< HEAD
from ingenieria_web.social.models import UserGrupos, Grupo
=======
from ingenieria_web.social.forms import NuevoGrupo
from ingenieria_web.social.models import Suscripcion
>>>>>>> 51305ad6fe36c1285c76aa712854079314afba0a
# Create your views here.

def search(request):
    q = request.GET.get('q')
    formNuevoGrupo = NuevoGrupo()
    listaSuscripciones = Suscripcion.objects.all().order_by('-fecha_peticion')
    if q:
        grupos = GrupoDocument.search().query("match", NombreGrupo=q)
    else:
        grupos = ''

<<<<<<< HEAD
    misGrupos = UserGrupos.objects.filter(idUser = request.user).values_list('idGrupoUsuario', flat=True)
    
    print(misGrupos)

    
    return render(request, 'adminlte/search.html', {'grupos':grupos, 'misGrupos':misGrupos})
=======
    return render(request, 'adminlte/search.html', {'grupos':grupos, 'formNuevoGrupo': formNuevoGrupo,'listaSuscripciones':listaSuscripciones})
>>>>>>> 51305ad6fe36c1285c76aa712854079314afba0a
