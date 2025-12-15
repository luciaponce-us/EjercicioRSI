#encoding:utf-8

from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator




class Anime(models.Model):
    """ Anime: Animeid, Título, Géneros, Formato de emisión (TV, movie,…), Número de episodios. """
    animeId = models.AutoField(primary_key=True, default=None)
    titulo = models.TextField(verbose_name='Título')
    generos = models.TextField(verbose_name='Géneros')
    formatoEmision = models.TextField(verbose_name='Formato de emisión', help_text='Ejemplo: TV, Movie, OVA, etc.')
    numeroEpisodios = models.IntegerField(verbose_name='Número de episodios', help_text='Debe introducir un número entero')

    def __str__(self):
        return self.titulo
    
    class Meta:
        ordering = ('titulo', )


class Puntuacion(models.Model):
    """ Puntuación: IdUsario, Animeid, Puntuación (1-10) """
    usuarioId = models.IntegerField(verbose_name='ID Usuario')
    animeId = models.ForeignKey(Anime, on_delete=models.CASCADE)
    puntuacion = models.IntegerField(
        verbose_name='Puntuación',
        validators=[MinValueValidator(1), MaxValueValidator(10)],
        help_text='Debe introducir un número entre 1 y 10'
    )

    def __str__(self):
        return f'Usuario {self.usuarioId} - Anime {self.animeId.titulo} - Puntuación {self.puntuacion}'
    
    class Meta:
        unique_together = ('usuarioId', 'animeId')
        ordering = ('-puntuacion', )
