from django.shortcuts import render
from django.core.paginator import Paginator
from .models import DadoDiario
from datetime import date, datetime, timedelta
from pytz import timezone
from django.views import View


class Queries:
    def _formatDate(self, format: str, datetimeObj: datetime):
        return datetimeObj.strftime(format)

    def _curretnYear(self):
        dateToday = str(datetime.now(timezone('America/Sao_Paulo')))
        dateToday = datetime.strptime(
            dateToday, '%Y-%m-%d %H:%M:%S.%f%z'
        )
        currentYear: str = dateToday.strftime('%Y')
        return currentYear

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

    def _retroactiveDate(self, numberDaysComeBack: int):
        dateToday = str(datetime.now(timezone('America/Sao_Paulo')))
        dateYesterday = datetime.strptime(
            dateToday, '%Y-%m-%d %H:%M:%S.%f%z'
        ) - timedelta(numberDaysComeBack)
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

    def queryFilterMaxByCurrentYear(self, collumn: str) -> tuple:
        currentYear = str(self._curretnYear())
        sql = f'SELECT codigo, dia, {collumn} FROM dado_diario' \
            f' WHERE {collumn}=' \
            f'(SELECT MAX({collumn}) FROM dado_diario WHERE EXTRACT(YEAR FROM(SELECT dia))=%s) AND' \
            ' EXTRACT(YEAR FROM(SELECT dia))=%s ORDER BY dia DESC'
        data: tuple = (currentYear, currentYear)
        return (sql, data)

    def queryFilterMinByCurrentYear(self, collumn: str) -> tuple:
        currentYear = str(self._curretnYear())
        sql = f'SELECT codigo, dia, {collumn} FROM dado_diario' \
            f' WHERE {collumn}=' \
            f'(SELECT MIN({collumn}) FROM dado_diario WHERE EXTRACT(YEAR FROM(SELECT dia))=%s) AND' \
            ' EXTRACT(YEAR FROM(SELECT dia))=%s ORDER BY dia DESC'
        data: tuple = (currentYear, currentYear)
        return (sql, data)

    def queryFilterMeanByCurrentYear(self, collumn: str):
        currentYear = self._curretnYear()
        sql = f'SELECT 1 AS codigo, AVG({collumn}) FROM' \
            ' dado_diario WHERE EXTRACT(YEAR FROM(SELECT dia))=%s'
        data: tuple = (currentYear, )
        return (sql, data)


class MyView(Queries):
    template_error = 'notfound/404.html'

    def myGet(self, request, numberPager: int):
        try:
            sql, data = self.queryMeanData()
            result = DadoDiario.objects.raw(sql, data)
            paginator = Paginator(result, numberPager)
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
            return (self.template_name, context)
        except Exception:
            return (self.template_error, {})

    def myPost(self, request, viewBdType: str):
        try:
            recept = request.POST
            dateStart = recept['date-start']
            dateEnd = recept['date-end']
            if not dateStart or not dateEnd:
                return (self.template_error, {})
            sql, data = self.queryFilterByDate(dateStart, dateEnd, viewBdType)
            result = DadoDiario.objects.raw(sql, data)
            self.checkDict['umi'] = 1 if 'check-umi' in recept else 0
            self.checkDict['press'] = 1 if 'check-press' in recept else 0
            self.checkDict['t1'] = 1 if 'check-t1' in recept else 0
            self.checkDict['t2'] = 1 if 'check-t2' in recept else 0
            context = {
                'pageObj': result,
                'actionUrl': self.action_url,
                'pUmi': self.checkDict['umi'],
                'pPress': self.checkDict['press'],
                'pT1': self.checkDict['t1'],
                'pT2': self.checkDict['t2'],
            }
            return (self.template_name, context)
        except Exception:
            return (self.template_error, {})


class PagesTableMeanView(View, MyView):
    template_name = 'registros/tabela/meantable.html'
    action_url = "/registros/tabela/medias"
    checkDict: dict = {
        'umi': 1,
        'press': 1,
        't1': 1,
        't2': 1,
    }

    def get(self, request):
        template, context = self.myGet(request, 30)
        return render(request, template, context)

    def post(self, request):
        template, context = self.myPost(request, 'medias')
        return render(request, template, context)


class PagesTablesMaxView(View, MyView):
    template_name = 'registros/tabela/maxtable.html'
    action_url = "/registros/tabela/maximos"
    checkDict: dict = {
        'umi': 1,
        'press': 1,
        't1': 1,
        't2': 1,
    }

    def get(self, request):
        template, context = self.myGet(request, 30)
        return render(request, template, context)

    def post(self, request):
        template, context = self.myPost(request, 'maximas')
        return render(request, template, context)


class PagesTablesMinView(View, MyView):
    template_name = 'registros/tabela/mintable.html'
    action_url = "/registros/tabela/minimos"
    checkDict: dict = {
        'umi': 1,
        'press': 1,
        't1': 1,
        't2': 1,
    }

    def get(self, request):
        template, context = self.myGet(request, 30)
        return render(request, template, context)

    def post(self, request):
        template, context = self.myPost(request, 'minimas')
        return render(request, template, context)


class PagesTablesMedianView(View, MyView):
    template_name = 'registros/tabela/mediantable.html'
    action_url = "/registros/tabela/medianas"
    checkDict: dict = {
        'umi': 1,
        'press': 1,
        't1': 1,
        't2': 1,
    }

    def get(self, request):
        template, context = self.myGet(request, 30)
        return render(request, template, context)

    def post(self, request):
        template, context = self.myPost(request, 'medianas')
        return render(request, template, context)


class PagesTablesModeView(View, MyView):
    template_name = 'registros/tabela/modetable.html'
    action_url = "/registros/tabela/modas"
    checkDict: dict = {
        'umi': 1,
        'press': 1,
        't1': 1,
        't2': 1,
    }

    def get(self, request):
        template, context = self.myGet(request, 30)
        return render(request, template, context)

    def post(self, request):
        template, context = self.myPost(request, 'modas')
        return render(request, template, context)


class PagesGraphsView(View):
    pass


class PageIndexView(View, Queries):
    template_name = 'index/index.html'
    template_error = 'notfound/404.html'

    def get(self, request):
        try:
            currentYear = self._curretnYear()

            sql, data = self.queryFilterMaxByCurrentYear(
                'maximo_temp_ext'
            )
            resultMaxTemp = DadoDiario.objects.raw(sql, data)

            sql, data = self.queryFilterMinByCurrentYear(
                'minimo_temp_ext'
            )
            resultMinTemp = DadoDiario.objects.raw(sql, data)

            sql, data = self.queryFilterMeanByCurrentYear('media_temp_ext')
            resultMeanTemp = DadoDiario.objects.raw(sql, data)

            sql, data = self.queryFilterMaxByCurrentYear(
                'maximo_umidade'
            )
            resultMaxUmi = DadoDiario.objects.raw(sql, data)

            sql, data = self.queryFilterMinByCurrentYear(
                'minimo_umidade'
            )
            resultMinUmi = DadoDiario.objects.raw(sql, data)

            sql, data = self.queryFilterMeanByCurrentYear('media_umidade')
            resultMeanUmi = DadoDiario.objects.raw(sql, data)

            sql, data = self.queryFilterMaxByCurrentYear(
                'maximo_pressao'
            )
            resultMaxPress = DadoDiario.objects.raw(sql, data)

            sql, data = self.queryFilterMinByCurrentYear(
                'minimo_pressao'
            )
            resultMinPress = DadoDiario.objects.raw(sql, data)

            sql, data = self.queryFilterMeanByCurrentYear('media_pressao')
            resultMeanPress = DadoDiario.objects.raw(sql, data)
            counter = 0
            context = {
                'resultMaxTemp': list(resultMaxTemp),
                'resultMinTemp': resultMinTemp,
                'resultMeanTemp': resultMeanTemp,
                'resultMaxUmi': resultMaxUmi,
                'resultMinUmi': resultMinUmi,
                'resultMeanUmi': resultMeanUmi,
                'resultMaxPress': resultMaxPress,
                'resultMinPress': resultMinPress,
                'resultMeanPress': resultMeanPress,
                'currentYear': currentYear,
                'counter': counter,
            }
            return render(request, self.template_name, context)
        except Exception as e:
            print(e.__class__.__name__, e)
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
