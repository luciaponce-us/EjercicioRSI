from django.contrib import admin
from django.urls import path
from main import views

urlpatterns = [
    path('',views.index),
    path('index.html/', views.index),
    path('populate/', views.populateDatabase),
    path('loadRS/', views.loadRS),  
    path('admin/',admin.site.urls),
    path('animes_por_formato_de_emision/', views.animes_por_formato, name='animes_por_formato_de_emision'),
    path('animes_mas_populares/', views.animes_mas_populares, name='animes_mas_populares'),
    path('recomendar_usuarios/', views.animes_por_formato, name='recomendar_usuarios'),

    ]
