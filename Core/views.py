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
        data: list = [f"{self.__dateYesterday()} 00:00:00"]
        return (sql, data)


class PagesTableMeanView(View):
    template_name = 'registros/tabela/meantable.html'

    def get(self, request):
        data = DadoDiario.objects.order_by('-dia')
        paginator = Paginator(data, 10)
        pageNumber = request.GET.get("page")
        pageObj = paginator.get_page(pageNumber)
        context = {
            'pageObj': pageObj,
        }
        return render(request, self.template_name, context)


class PagesTablesMaxView(View):

    def tableMax(self, request):
        pass


class PagesTablesMinView(View):

    def tableMin(self, request):
        pass


class PagesTablesMedianView(View):

    def tableMedian(self, request):
        pass


class PagesTablesModeView(View):

    def tableMode(self, request):
        pass


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


class PageMainRegisters(View):
    template_name = 'registros/menuRegistros.html'

    def get(self, request):
        yDate = Queries()
        query, data = yDate.queryDateYesterday()
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
