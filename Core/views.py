from django.shortcuts import render
from django.core.paginator import Paginator
from .models import DadoDiario
from datetime import date, datetime, timedelta
from pytz import timezone
from django.views import View


class Queries:
    def __dateYesterday(self):
        dateToday = str(datetime.now(timezone('America/Sao_Paulo')))
        dateYesterday = datetime.strptime(
            dateToday, '%Y-%m-%d %H:%M:%S.%f%z'
        ) - timedelta(1)
        dayYesterday: int = int(dateYesterday.strftime('%d'))
        monthYesterday: int = int(dateYesterday.strftime('%m'))
        yearYesterday: int = int(dateYesterday.strftime('%Y'))
        queryDate = date(yearYesterday, monthYesterday, dayYesterday)
        return queryDate

    def queryDateYesterday(self) -> tuple:
        sql = 'SELECT * FROM dado_diario WHERE dia=%s'
        data: tuple = (f"{self.__dateYesterday()} 00:00:00", )
        return (sql, data)

    def queryMinData(self) -> tuple:
        sql = 'SELECT * FROM minimas_totais'
        data: tuple = ()
        return (sql, data)

    def queryMaxData(self) -> tuple:
        sql = 'SELECT * FROM maximas_totais'
        data: tuple = ()
        return (sql, data)

    def queryMeanData(self) -> tuple:
        sql = 'SELECT * FROM medias_totais'
        data: tuple = ()
        return (sql, data)

    def queryMedianData(self) -> tuple:
        sql = 'SELECT * FROM medianas_totais'
        data: tuple = ()
        return (sql, data)

    def queryModeData(self) -> tuple:
        sql = 'SELECT * FROM modas_totais'
        data: tuple = ()
        return (sql, data)


class PagesTableMeanView(View, Queries):
    template_name = 'registros/tabela/meantable.html'

    def get(self, request):
        sql, data = self.queryMeanData()
        result = DadoDiario.objects.raw(sql, data)
        paginator = Paginator(result, 30)
        pageNumber = request.GET.get("page")
        pageObj = paginator.get_page(pageNumber)
        context = {
            'pageObj': pageObj,
        }
        return render(request, self.template_name, context)


class PagesTablesMaxView(View, Queries):
    template_name = 'registros/tabela/maxtable.html'

    def get(self, request):
        sql, data = self.queryMaxData()
        result = DadoDiario.objects.raw(sql, data)
        paginator = Paginator(result, 30)
        pageNumber = request.GET.get("page")
        pageObj = paginator.get_page(pageNumber)
        context = {
            'pageObj': pageObj,
        }
        return render(request, self.template_name, context)


class PagesTablesMinView(View, Queries):
    template_name = 'registros/tabela/mintable.html'

    def get(self, request):
        sql, data = self.queryMinData()
        result = DadoDiario.objects.raw(sql, data)
        paginator = Paginator(result, 30)
        pageNumber = request.GET.get("page")
        pageObj = paginator.get_page(pageNumber)
        context = {
            'pageObj': pageObj,
        }
        return render(request, self.template_name, context)


class PagesTablesMedianView(View, Queries):
    template_name = 'registros/tabela/mediantable.html'

    def get(self, request):
        sql, data = self.queryMedianData()
        result = DadoDiario.objects.raw(sql, data)
        paginator = Paginator(result, 30)
        pageNumber = request.GET.get("page")
        pageObj = paginator.get_page(pageNumber)
        context = {
            'pageObj': pageObj,
        }
        return render(request, self.template_name, context)


class PagesTablesModeView(View, Queries):
    template_name = 'registros/tabela/modetable.html'

    def get(self, request):
        sql, data = self.queryModeData()
        result = DadoDiario.objects.raw(sql, data)
        paginator = Paginator(result, 30)
        pageNumber = request.GET.get("page")
        pageObj = paginator.get_page(pageNumber)
        context = {
            'pageObj': pageObj,
        }
        return render(request, self.template_name, context)


class PagesGraphsView(View):
    pass


class PageIndexView(View):
    template_name = 'index/index.html'

    def get(self, request):
        return render(request, self.template_name)


class PageAboutView(View):
    template_name = 'sobre/sobre.html'

    def get(self, request):
        return render(request, self.template_name)


class PageMainRegisters(View, Queries):
    template_name = 'registros/menuRegistros.html'

    def get(self, request):
        query, data = self.queryDateYesterday()
        dateToday = DadoDiario.objects.raw(query, data)
        context = {
            'dateToday': dateToday,
        }
        return render(request, self.template_name, context)


class PageMainTables(View):
    template_name = 'registros/tabela/tabela.html'

    def get(self, request):
        return render(request, self.template_name)


class PageMainGraphs(View):
    template_name = 'registros/graficos/grafico.html'

    def get(self, request):
        return render(request, self.template_name)
