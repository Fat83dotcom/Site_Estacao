from django.shortcuts import render
from .models import DadoDiario


def index(request):
    return render(request, 'index/index.html')


def lista(request):
    dado = DadoDiario.objects.order_by('-dia')
    context = {
        'dado': dado
    }
    return render(request, 'graficos/lista.html', context)


def sobre(request):
    return render(request, 'sobre/sobre.html')
