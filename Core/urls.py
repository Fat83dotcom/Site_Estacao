from django.urls import path
from Core import views

urlpatterns = [
    path('', views.index, name='index'),
    path('registros/', views.registros, name='registros'),
    path('registros/tabela', views.tabela, name='tabela'),
    path('registros/graficos', views.graficos, name='graficos'),
    path('sobre/', views.sobre, name='sobre'),
]
