from django.urls import path
from Core import views

urlpatterns = [
    path('', views.PageIndexView.as_view(), name='index'),
    path('registros/', views.PageMainRegisters.as_view(), name='registros'),
    path('registros/tabela', views.PageMainTables.as_view(), name='tabela'),
    path(
        'registros/tabela/medias',
        views.PagesTableMeanView.as_view(),
        name='tabelamedia'
    ),
    path(
        'registros/tabela/minimos',
        views.PagesTablesMinView.as_view(),
        name='tabelamin'
    ),
    path(
        'registros/tabela/maximos',
        views.PagesTablesMaxView.as_view(),
        name='tabelamax'
    ),
    path(
        'registros/tabela/medianas',
        views.PagesTablesMedianView.as_view(),
        name='tabelamediana'
    ),
    path(
        'registros/tabela/modas',
        views.PagesTablesModeView.as_view(),
        name='tabelamoda'
    ),
    path(
        'registros/graficos',
        views.PageMainGraphs.as_view(),
        name='graficos'
    ),
    path('sobre/', views.PageAboutView.as_view(), name='sobre'),
    path('error/', views.PageError.as_view(), name='error'),
]
