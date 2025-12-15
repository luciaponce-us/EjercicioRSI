from django.conf import settings
from main.forms_lucia import FormatoEmisionForm
from main.models import Anime
from django.shortcuts import render

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