from django.urls import path
from Core import views

urlpatterns = [
    path('', views.index, name='index'),
    path('lista/', views.lista, name='lista'),
    path('sobre/', views.sobre, name='sobre'),
]
