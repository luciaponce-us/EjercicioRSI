from django.conf import settings
from main.models import Anime, Puntuacion
from main.forms import ConfirmarCarga, FormatoEmisionForm
from django.shortcuts import render
import shelve
from main.recommendations import  transformPrefs, calculateSimilarItems
from main.populateDB import populate
from django.http.response import HttpResponseRedirect
from django.db.models import Count

def index(request):
    return render(request, 'index.html', {'STATIC_URL': settings.STATIC_URL})

def loadDict():
    Prefs={}   # matriz de usuarios y puntuaciones a cada a items
    shelf = shelve.open("dataRS.dat")
    ratings = Puntuacion.objects.all()
    for ra in ratings:
        usuario = int(ra.usuarioId)
        anime = int(ra.animeId.animeId)
        puntuacion = float(ra.puntuacion)
        Prefs.setdefault(usuario, {})
        Prefs[usuario][anime] = puntuacion
    shelf['Prefs']=Prefs
    shelf['AnimePrefs']=transformPrefs(Prefs)
    shelf['SimItems']=calculateSimilarItems(Prefs, n=10)
    shelf.close()

def loadRS(request):
    loadDict()
    return HttpResponseRedirect('/index.html')

def populateDatabase(request):
    mensaje = ''
    formulario = ConfirmarCarga()
    if request.method=='POST':
        formulario = ConfirmarCarga(request.POST)
        if formulario.is_valid():
            mensaje = populate()
    return render(request, 'index.html', {'formulario': formulario, 'finalizado': mensaje, 'STATIC_URL':settings.STATIC_URL})


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


def animes_mas_populares(request):
    animes_mejor_valorados = Puntuacion.objects.values('animeId').annotate(num_votos=Count('animeId')).order_by('-num_votos')[:3]
    shelf = shelve.open("dataRS.dat")
    Animesimilares = shelf['SimItems']
    shelf.close()
    resultados = []

    for anime in animes_mejor_valorados:
        AnimesParecidos = Animesimilares.get(anime['animeId'], [])[:3]
        
        similares = []
        for similitud, anime_similar_id in AnimesParecidos:
            try:
                anime_obj = Anime.objects.get(animeId=anime_similar_id)
                similares.append({
                    'anime': anime_obj,
                    'similitud': similitud
                })
            except Anime.DoesNotExist:
                continue

        resultados.append({
            'anime': Anime.objects.get(animeId=anime['animeId']),
            'similares': similares
        })

    return render(request, 'animes_mas_populares.html', {
        'resultados': resultados,
        'STATIC_URL': settings.STATIC_URL
    })