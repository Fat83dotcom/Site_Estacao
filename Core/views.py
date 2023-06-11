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

    def queryFilterByDate(
        self, dateStart: str, dateEnd: str, viewBdType: str
    ) -> tuple:
        sql = f'SELECT * FROM {viewBdType}_totais WHERE dia BETWEEN %s AND %s'
        data: tuple = (dateStart, dateEnd)
        return (sql, data)


class PagesTableMeanView(View, Queries):
    template_name = 'registros/tabela/meantable.html'
    template_error = 'notfound/404.html'
    action_url = "/registros/tabela/medias"
    checkDict: dict = {
        'umi': 1,
        'press': 1,
        't1': 1,
        't2': 1,
    }

    def get(self, request):
        try:
            sql, data = self.queryMeanData()
            result = DadoDiario.objects.raw(sql, data)
            paginator = Paginator(result, 30)
            pageNumber = request.GET.get("page")
            pageObj = paginator.get_page(pageNumber)
            context = {
                'pageObj': pageObj,
                'actionUrl': self.action_url,
                'pUmi': self.checkDict['umi'],
                'pPress': self.checkDict['press'],
                'pT1': self.checkDict['t1'],
                'pT2': self.checkDict['t2'],
            }
            return render(request, self.template_name, context)
        except Exception as e:
            print(e.__class__.__name__, e)
            return render(request, self.template_error)

    def post(self, request):
        try:
            recept = request.POST
            dateStart = recept['date-start']
            dateEnd = recept['date-end']
            sql, data = self.queryFilterByDate(dateStart, dateEnd, 'medias')
            result = DadoDiario.objects.raw(sql, data)
            paginator = Paginator(result, 30)
            pageNumber = request.POST.get("page")
            pageObj = paginator.get_page(pageNumber)
            self.checkDict['umi'] = 1 if 'check-umi' in recept else 0
            self.checkDict['press'] = 1 if 'check-press' in recept else 0
            self.checkDict['t1'] = 1 if 'check-t1' in recept else 0
            self.checkDict['t2'] = 1 if 'check-t2' in recept else 0
            context = {
                'pageObj': pageObj,
                'actionUrl': self.action_url,
                'pUmi': self.checkDict['umi'],
                'pPress': self.checkDict['press'],
                'pT1': self.checkDict['t1'],
                'pT2': self.checkDict['t2'],
            }
            return render(request, self.template_name, context)
        except Exception as e:
            print(e.__class__.__name__, e)
            return render(request, self.template_name)


class PagesTablesMaxView(View, Queries):
    template_name = 'registros/tabela/maxtable.html'
    template_error = 'notfound/404.html'
    action_url = "/registros/tabela/maximos"
    checkDict: dict = {
        'umi': 1,
        'press': 1,
        't1': 1,
        't2': 1,
    }

    def get(self, request):
        try:
            sql, data = self.queryMeanData()
            result = DadoDiario.objects.raw(sql, data)
            paginator = Paginator(result, 30)
            pageNumber = request.GET.get("page")
            pageObj = paginator.get_page(pageNumber)
            context = {
                'pageObj': pageObj,
                'actionUrl': self.action_url,
                'pUmi': self.checkDict['umi'],
                'pPress': self.checkDict['press'],
                'pT1': self.checkDict['t1'],
                'pT2': self.checkDict['t2'],
            }
            return render(request, self.template_name, context)
        except Exception as e:
            print(e.__class__.__name__, e)
            return render(request, self.template_error)

    def post(self, request):
        try:
            recept = request.POST
            dateStart = recept['date-start']
            dateEnd = recept['date-end']
            sql, data = self.queryFilterByDate(dateStart, dateEnd, 'maximas')
            result = DadoDiario.objects.raw(sql, data)
            paginator = Paginator(result, 30)
            pageNumber = request.POST.get("page")
            pageObj = paginator.get_page(pageNumber)
            self.checkDict['umi'] = 1 if 'check-umi' in recept else 0
            self.checkDict['press'] = 1 if 'check-press' in recept else 0
            self.checkDict['t1'] = 1 if 'check-t1' in recept else 0
            self.checkDict['t2'] = 1 if 'check-t2' in recept else 0
            context = {
                'pageObj': pageObj,
                'actionUrl': self.action_url,
                'pUmi': self.checkDict['umi'],
                'pPress': self.checkDict['press'],
                'pT1': self.checkDict['t1'],
                'pT2': self.checkDict['t2'],
            }
            return render(request, self.template_name, context)
        except Exception as e:
            print(e)
            return render(request, self.template_name)


class PagesTablesMinView(View, Queries):
    template_name = 'registros/tabela/mintable.html'
    template_error = 'notfound/404.html'
    action_url = "/registros/tabela/minimos"
    checkDict: dict = {
        'umi': 1,
        'press': 1,
        't1': 1,
        't2': 1,
    }

    def get(self, request):
        try:
            sql, data = self.queryMeanData()
            result = DadoDiario.objects.raw(sql, data)
            paginator = Paginator(result, 30)
            pageNumber = request.GET.get("page")
            pageObj = paginator.get_page(pageNumber)
            context = {
                'pageObj': pageObj,
                'actionUrl': self.action_url,
                'pUmi': self.checkDict['umi'],
                'pPress': self.checkDict['press'],
                'pT1': self.checkDict['t1'],
                'pT2': self.checkDict['t2'],
            }
            return render(request, self.template_name, context)
        except Exception as e:
            print(e.__class__.__name__, e)
            return render(request, self.template_error)

    def post(self, request):
        try:
            recept = request.POST
            dateStart = recept['date-start']
            dateEnd = recept['date-end']
            sql, data = self.queryFilterByDate(dateStart, dateEnd, 'minimas')
            result = DadoDiario.objects.raw(sql, data)
            paginator = Paginator(result, 30)
            pageNumber = request.POST.get("page")
            pageObj = paginator.get_page(pageNumber)
            self.checkDict['umi'] = 1 if 'check-umi' in recept else 0
            self.checkDict['press'] = 1 if 'check-press' in recept else 0
            self.checkDict['t1'] = 1 if 'check-t1' in recept else 0
            self.checkDict['t2'] = 1 if 'check-t2' in recept else 0
            context = {
                'pageObj': pageObj,
                'actionUrl': self.action_url,
                'pUmi': self.checkDict['umi'],
                'pPress': self.checkDict['press'],
                'pT1': self.checkDict['t1'],
                'pT2': self.checkDict['t2'],
            }
            return render(request, self.template_name, context)
        except Exception as e:
            print(e)
            return render(request, self.template_name)


class PagesTablesMedianView(View, Queries):
    template_name = 'registros/tabela/mediantable.html'
    template_error = 'notfound/404.html'
    action_url = "/registros/tabela/medianas"
    checkDict: dict = {
        'umi': 1,
        'press': 1,
        't1': 1,
        't2': 1,
    }

    def get(self, request):
        try:
            sql, data = self.queryMeanData()
            result = DadoDiario.objects.raw(sql, data)
            paginator = Paginator(result, 30)
            pageNumber = request.GET.get("page")
            pageObj = paginator.get_page(pageNumber)
            context = {
                'pageObj': pageObj,
                'actionUrl': self.action_url,
                'pUmi': self.checkDict['umi'],
                'pPress': self.checkDict['press'],
                'pT1': self.checkDict['t1'],
                'pT2': self.checkDict['t2'],
            }
            return render(request, self.template_name, context)
        except Exception as e:
            print(e.__class__.__name__, e)
            return render(request, self.template_error)

    def post(self, request):
        try:
            recept = request.POST
            dateStart = recept['date-start']
            dateEnd = recept['date-end']
            sql, data = self.queryFilterByDate(dateStart, dateEnd, 'medianas')
            result = DadoDiario.objects.raw(sql, data)
            paginator = Paginator(result, 30)
            pageNumber = request.POST.get("page")
            pageObj = paginator.get_page(pageNumber)
            self.checkDict['umi'] = 1 if 'check-umi' in recept else 0
            self.checkDict['press'] = 1 if 'check-press' in recept else 0
            self.checkDict['t1'] = 1 if 'check-t1' in recept else 0
            self.checkDict['t2'] = 1 if 'check-t2' in recept else 0
            context = {
                'pageObj': pageObj,
                'actionUrl': self.action_url,
                'pUmi': self.checkDict['umi'],
                'pPress': self.checkDict['press'],
                'pT1': self.checkDict['t1'],
                'pT2': self.checkDict['t2'],
            }
            return render(request, self.template_name, context)
        except Exception as e:
            print(e)
            return render(request, self.template_name)


class PagesTablesModeView(View, Queries):
    template_name = 'registros/tabela/modetable.html'
    template_error = 'notfound/404.html'
    action_url = "/registros/tabela/modas"
    checkDict: dict = {
        'umi': 1,
        'press': 1,
        't1': 1,
        't2': 1,
    }

    def get(self, request):
        try:
            sql, data = self.queryMeanData()
            result = DadoDiario.objects.raw(sql, data)
            paginator = Paginator(result, 30)
            pageNumber = request.GET.get("page")
            pageObj = paginator.get_page(pageNumber)
            context = {
                'pageObj': pageObj,
                'actionUrl': self.action_url,
                'pUmi': self.checkDict['umi'],
                'pPress': self.checkDict['press'],
                'pT1': self.checkDict['t1'],
                'pT2': self.checkDict['t2'],
            }
            return render(request, self.template_name, context)
        except Exception as e:
            print(e.__class__.__name__, e)
            return render(request, self.template_error)

    def post(self, request):
        try:
            recept = request.POST
            dateStart = recept['date-start']
            dateEnd = recept['date-end']
            sql, data = self.queryFilterByDate(dateStart, dateEnd, 'modas')
            result = DadoDiario.objects.raw(sql, data)
            paginator = Paginator(result, 30)
            pageNumber = request.POST.get("page")
            pageObj = paginator.get_page(pageNumber)
            self.checkDict['umi'] = 1 if 'check-umi' in recept else 0
            self.checkDict['press'] = 1 if 'check-press' in recept else 0
            self.checkDict['t1'] = 1 if 'check-t1' in recept else 0
            self.checkDict['t2'] = 1 if 'check-t2' in recept else 0
            context = {
                'pageObj': pageObj,
                'actionUrl': self.action_url,
                'pUmi': self.checkDict['umi'],
                'pPress': self.checkDict['press'],
                'pT1': self.checkDict['t1'],
                'pT2': self.checkDict['t2'],
            }
            return render(request, self.template_name, context)
        except Exception as e:
            print(e)
            return render(request, self.template_name)


class PagesGraphsView(View):
    pass


class PageIndexView(View):
    template_name = 'index/index.html'
    template_error = 'notfound/404.html'

    def get(self, request):
        try:
            return render(request, self.template_name)
        except Exception:
            return render(request, self.template_error)


class PageAboutView(View):
    template_name = 'sobre/sobre.html'
    template_error = 'notfound/404.html'

    def get(self, request):
        try:
            return render(request, self.template_name)
        except Exception:
            return render(request, self.template_error)


class PageMainRegisters(View, Queries):
    template_name = 'registros/menuRegistros.html'
    template_error = 'notfound/404.html'

    def get(self, request):
        try:
            query, data = self.queryDateYesterday()
            dateToday = DadoDiario.objects.raw(query, data)
            context = {
                'dateToday': dateToday,
            }
            return render(request, self.template_name, context)
        except Exception:
            return render(request, self.template_error)

    def post(self, request):
        return render(request, self.template_error)


class PageMainTables(View):
    template_name = 'registros/tabela/tabela.html'
    template_error = 'notfound/404.html'

    def get(self, request):
        return render(request, self.template_name)

    def post(self, request):
        return render(request, self.template_error)


class PageMainGraphs(View):
    template_name = 'registros/graficos/grafico.html'
    template_error = 'notfound/404.html'

    def get(self, request):
        return render(request, self.template_name)


class PageError(View):
    template_name = 'notfound/404.html'

    def get(self, request):
        return render(request, self.template_name)
