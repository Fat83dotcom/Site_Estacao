from django.urls import path
from Core.Views import api


urlpatterns = [
    path('tempo_real/', api.lastDailyEntry, name='tempoReal'),
]
