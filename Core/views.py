from django.shortcuts import render
from django.core.paginator import Paginator
from .models import DadoDiario


def index(request):
    return render(request, 'index/index.html')


def tabela(request):
    data = DadoDiario.objects.order_by('-dia')
    paginator = Paginator(data, 10)
    pageNumber = request.GET.get("page")
    pageObj = paginator.get_page(pageNumber)
    context = {
        'pageObj': pageObj,
    }
    return render(request, 'registros/tabela/tabela.html', context)


def registros(request):
    query, data = queryDateYesterday()
    dateToday = DadoDiario.objects.raw(query, data)
    context = {
        'dado': dado
    }
    return render(request, 'graficos/lista.html', context)


def sobre(request):
    return render(request, 'sobre/sobre.html')
