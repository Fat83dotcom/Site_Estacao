from django.shortcuts import render
from django.core.paginator import Paginator
from .models import DadoDiario
from datetime import date, datetime, timedelta
from pytz import timezone


def queryDateYesterday() -> str:
    dateToday = str(datetime.now(timezone('America/Sao_Paulo')))
    dateYesterday = datetime.strptime(
        dateToday, '%Y-%m-%d %H:%M:%S.%f%z'
    ) - timedelta(1)
    dayYesterday: int = int(dateYesterday.strftime('%d'))
    monthYesterday: int = int(dateYesterday.strftime('%m'))
    yearYesterday: int = int(dateYesterday.strftime('%Y'))
    queryDate = date(yearYesterday, monthYesterday, dayYesterday)
    sql = 'SELECT * FROM dado_diario WHERE dia=%s'
    data: list = [f"{queryDate} 00:00:00"]
    return (sql, data)


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
        'dateToday': dateToday,
    }
    for i in dateToday:
        print(i)
    return render(request, 'registros/menuRegistros.html', context)


def graficos(request):
    return render(request, 'registros/graficos/grafico.html')


def sobre(request):
    return render(request, 'sobre/sobre.html')
