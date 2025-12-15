from main.models import Anime, Puntuacion
from datetime import datetime

path = "data"

def populate():
    populateAnime()
    populatePuntuaciones() 
    print("Base de datos poblada con éxito.")

def populateAnime():
    if Anime.objects.exists():
        Anime.objects.all().delete()

    lista=[]
    fileobj=open(path+"\\anime.txt", "r", encoding='utf-8')
    for line in fileobj.readlines()[1:]: 
        rip = str(line.strip()).split('\t')
        if len(rip) != 5:
            continue

        if rip[4]=='Unknown':
            rip[4]=0
        a = Anime(animeId=rip[0], titulo=rip[1], generos=rip[2], formatoEmision=rip[3], numeroEpisodios=int(rip[4]))
        lista.append(a)
    fileobj.close()
    Anime.objects.bulk_create(lista)

    return(lista)

def populatePuntuaciones():
    if Puntuacion.objects.exists():
        Puntuacion.objects.all().delete()

    lista=[]
    fileobj=open(path+"\\ratings.txt", "r", encoding='utf-8')
    for line in fileobj.readlines()[1:]:
        rip = str(line.strip()).split('\t')
        if len(rip) != 3:
            continue

        p = Puntuacion(usuarioId=int(rip[0]), animeId=Anime.objects.get(animeId=int(rip[1])), puntuacion=int(rip[2]))
        lista.append(p)
    fileobj.close()
    Puntuacion.objects.bulk_create(lista)
    return(lista)
