from django.urls import path
from Core import views

urlpatterns = [
    path('', views.PageIndexView.as_view(), name='index'),
    path('registros/', views.PageMainRegisters.as_view(), name='registros'),
    path('registros/tabela', views.PageMainTables.as_view(), name='tabela'),
    path(
        'registros/tabela/medias',
        views.PagesTableMeanView.as_view(),
        name='tabelamedias'
    ),
    # path(),
    # path(),
    # path(),
    # path(),
    path(
        'registros/graficos',
        views.PageMainGraphs.as_view(),
        name='graficos'
    ),
    path('sobre/', views.PageAboutView.as_view(), name='sobre'),
]
