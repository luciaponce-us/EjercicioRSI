from main.models import Anime, Puntuacion
from datetime import datetime

path = "data"

def populate():
    populateAnime()
    populatePuntuaciones() 

def populateAnime():
    Anime.objects.all().delete()

    lista=[]
    fileobj=open(path+"\\anime.txt", "r", encoding='utf-8')
    for line in fileobj.readlines():
        rip = str(line.strip()).split('\t')
        if len(rip) != 5:
            continue

        a = Anime(animeId=rip[0], titulo=rip[1], generos=rip[2], formatoEmision=parsearGeneros(rip[3]), numeroEpisodios=int(rip[4]))
        lista.append(a)
    fileobj.close()
    Anime.objects.bulk_create(lista)

    return(lista)

def parsearGeneros(generosStr):
    generos = generosStr.split(',')
    listaGeneros = []
    for genero in generos:
        genero = genero.strip()
        listaGeneros.append(genero)
    return listaGeneros

def populatePuntuaciones():
    Puntuacion.objects.all().delete()

    lista=[]
    fileobj=open(path+"\\ratings.txt", "r", encoding='utf-8')
    for line in fileobj.readlines():
        rip = str(line.strip()).split('\t')
        if len(rip) != 3:
            continue

        p = Puntuacion(usuarioId=int(rip[0]), animeId=Anime.objects.get(animeId=int(rip[1])), puntuacion=int(rip[2]))
        lista.append(p)
    fileobj.close()
    Puntuacion.objects.bulk_create(lista)
    return(lista)
