from django.urls import path
from Core.Views import api


urlpatterns = [
    path('tempo_real/', api.LastEntry.as_view(), name='tempoReal'),
    path('graficosIndex/', api.Last24HoursEntry.as_view(), name='grafIndex'),
]
