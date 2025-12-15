from django.conf import settings
from main.models import Anime, Puntuacion
from main.forms import ConfirmarCarga, FormatoEmisionForm
from django.shortcuts import render
import shelve
from main.recommendations import  transformPrefs, calculateSimilarItems
from main.populateDB import populate
from django.http.response import HttpResponseRedirect


def index(request):
    return render(request, 'index.html', {'STATIC_URL': settings.STATIC_URL})

def loadDict():
    Prefs={}   # matriz de usuarios y puntuaciones a cada a items
    shelf = shelve.open("dataRS.dat")
    ratings = Puntuacion.objects.all()
    for ra in ratings:
        user = int(ra.idUsuario.idUsuario)
        itemid = int(ra.idPelicula.idPelicula)
        rating = float(ra.puntuacion)
        Prefs.setdefault(user, {})
        Prefs[user][itemid] = rating
    shelf['Prefs']=Prefs
    shelf['ItemsPrefs']=transformPrefs(Prefs)
    shelf['SimItems']=calculateSimilarItems(Prefs, n=10)
    shelf.close()


def populateDatabase(request):
    formulario = ConfirmarCarga()
    if request.method=='POST':
        formulario = ConfirmarCarga(request.POST)
        if formulario.is_valid():
            populate()
            return HttpResponseRedirect('/index.html')
    return render(request, 'index.html', {'formulario': formulario, 'STATIC_URL':settings.STATIC_URL})


def animes_por_formato(request):
    """
    Muestre un formulario con una spinbox con la lista de formatos de emisión que hay en la BD. Cuando se seleccione
    uno muestra el total de animes con ese formato de emisión y los datos de cada uno
    (Título, Géneros, Formato de emisión y Número de episodios) ordenados por número de
    episodios de mayor a menor.
    """
    form = FormatoEmisionForm()
    animes = []
    formato_seleccionado = None
    formatos = Anime.objects.values_list('formatoEmision', flat=True).distinct()
    total_animes = 0
    
    if request.method == 'POST':
        form = FormatoEmisionForm(request.POST)
        if form.is_valid():
            formato_seleccionado = form.cleaned_data['formatoEmision']
            animes = Anime.objects.filter(formatoEmision=formato_seleccionado).order_by('numeroEpisodios')
            total_animes = animes.count()
    
    return render(request, 'animes_por_formato.html', {
        'STATIC_URL': settings.STATIC_URL,
        'form': form,
        'animes': animes,
        'total_animes': total_animes,
        'formato_seleccionado': formato_seleccionado
    })