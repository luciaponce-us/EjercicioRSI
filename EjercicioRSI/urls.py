from django.contrib import admin
from django.urls import path
from main import views

urlpatterns = [
    path('',views.index),
    path('index.html/', views.index),
    path('populate/', views.populateDatabase),
    path('animes_por_formato/', views.animes_por_formato, name='animes_por_formato'),
    ]
