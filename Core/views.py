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

    def queryFilterColumnByDate(
        self, dateStart: str,
        dateEnd: str,
        viewBdType: str,
        collumn: str,
        ordering='DESC'
    ) -> tuple:
        sql = f'SELECT codigo, {collumn} FROM {viewBdType} WHERE dia BETWEEN %s AND %s' \
            f' ORDER BY dia {ordering}'
        data: tuple = (dateStart, dateEnd)
        return (sql, data)

    def queryFilterMaxByCurrentYear(
        self, collumn: str, ordering='DESC'
    ) -> tuple:
        currentYear = str(self._curretnYear())
        sql = f'SELECT codigo, dia, {collumn} FROM dado_diario' \
            f' WHERE {collumn}=' \
            f'(SELECT MAX({collumn}) FROM dado_diario WHERE EXTRACT(YEAR FROM(SELECT dia))=%s) AND' \
            f' EXTRACT(YEAR FROM(SELECT dia))=%s ORDER BY dia {ordering}'
        data: tuple = (currentYear, currentYear)
        return (sql, data)

    def queryFilterMinByCurrentYear(
        self, collumn: str, ordering='DESC'
    ) -> tuple:
        currentYear = str(self._curretnYear())
        sql = f'SELECT codigo, dia, {collumn} FROM dado_diario' \
            f' WHERE {collumn}=' \
            f'(SELECT MIN({collumn}) FROM dado_diario WHERE EXTRACT(YEAR FROM(SELECT dia))=%s) AND' \
            f' EXTRACT(YEAR FROM(SELECT dia))=%s ORDER BY dia {ordering}'
        data: tuple = (currentYear, currentYear)
        return (sql, data)

    def queryFilterMeanByCurrentYear(self, collumn: str):
        currentYear = self._curretnYear()
        sql = f'SELECT 1 AS codigo, AVG({collumn}) FROM' \
            ' dado_diario WHERE EXTRACT(YEAR FROM(SELECT dia))=%s'
        data: tuple = (currentYear, )
        return (sql, data)

    def queryFilterDateRange(
        self, dateStart: str,
        dateEnd: str,
        viewBdType='label_datas',
        ordering='DESC'
    ) -> tuple:
        sql = f'SELECT * FROM {viewBdType} WHERE dia BETWEEN %s AND %s' \
            f' ORDER BY dia {ordering}'
        data: tuple = (dateStart, dateEnd)
        return (sql, data)


class ManagerGraphs(Queries):
    colors = {
        'Umidade': {
            'maximas': 'rgba(92, 88, 11, 1)',
            'minimas': 'rgba(232, 222, 28, 1)',
            'medias': 'rgba(219, 211, 27, 1)',
            'medianas': 'rgba(156, 149, 19, 1)',
            'modas': 'rgba(194, 185, 23, 1)',
        },
        'Pressao': {
            'maximas': 'rgba(22, 92, 50, 1)',
            'minimas': 'rgba(56, 232, 126, 1)',
            'medias': 'rgba(37, 156, 85, 1)',
            'medianas': 'rgba(53, 219, 119, )',
            'modas': 'rgba(47, 194, 105, 1)',
        },
        'Temperatura-Interna': {
            'maximas': 'rgba(36, 34, 92, 1)',
            'minimas': 'rgba(91, 86, 232, 1)',
            'medias': 'rgba(61, 58, 156, 1)',
            'medianas': 'rgba(86, 82, 219, 1)',
            'modas': 'rgba(76, 72, 194, 1)',
        },
        'Temperatura-Externa': {
            'maximas': 'rgba(92, 17, 13, 1',
            'minimas': 'rgba(232, 42, 32, 1)',
            'medias': 'rgba(156, 28, 22, 1)',
            'medianas': 'rgba(220, 41, 31, 1)',
            'modas': 'rgba(194, 35, 27, 1)',
        }
    }

    def graph(self, physQuantity: str, meassure: str, data: list) -> dict:
        returnDataSet = {
            'label': f'{physQuantity} - {meassure}',
            'data': data,
            'backgroundColor': self.colors[physQuantity][meassure],
            'borderColor': '#000',
            'borderWidth': 1
        }
        return returnDataSet

    def dataGraph(
        self, dateStart: str,
        dateEnd: str,
        viewBdType: str,
        collumnBd: str
    ) -> list:
        try:
            extractData: list = []
            sql, data = self.queryFilterColumnByDate(
                dateStart, dateEnd, viewBdType, collumnBd, ordering='ASC'
            )
            result = DadoDiario.objects.raw(sql, data)
            for i in result:
                collumnValue = getattr(i, collumnBd)
                extractData.append(collumnValue)
            return extractData
        except Exception as e:
            print(e)
            raise e

    def labelGraph(self, dateStart: str, dateEnd: str) -> list:
        label: list = []
        sql, data = self.queryFilterDateRange(
            dateStart,
            dateEnd,
            ordering='ASC')
        result = DadoDiario.objects.raw(sql, data)
        for i in result:
            date = self._formatDate('%d/%m/%Y', i.dia)
            label.append(date)
        return label


class GraphsView(ManagerGraphs):
    template_error = 'notfound/404.html'
    collumnBdRelation = {
        'Umidade': {
            'medias': 'media_umidade',
            'maximas': 'maximo_umidade',
            'minimas': 'minimo_umidade',
            'medianas': 'mediana_umidade',
            'modas': 'moda_umidade'
        },
        'Pressao': {
            'medias': 'media_pressao',
            'maximas': 'maximo_pressao',
            'minimas': 'minimo_pressao',
            'medianas': 'mediana_pressao',
            'modas': 'moda_pressao'
        },
        'Temperatura-Interna': {
            'medias': 'media_temp_int',
            'maximas': 'maximo_temp_int',
            'minimas': 'minimo_temp_int',
            'medianas': 'mediana_temp_int',
            'modas': 'moda_temp_int'
        },
        'Temperatura-Externa': {
            'medias': 'media_temp_ext',
            'maximas': 'maximo_temp_ext',
            'minimas': 'minimo_temp_ext',
            'medianas': 'mediana_temp_ext',
            'modas': 'moda_temp_ext'
        },
    }
    meassures = ['medias', 'maximas', 'minimas', 'medianas', 'modas']

    def graphGet(self, request, graphType: str):
        startDate = self._retroactiveDate(5)
        endDate = self._retroactiveDate(1)
        dataSets: list = []
        labels: list = self.labelGraph(startDate, endDate)
        tempMeassure = ['maximas', 'minimas']
        for i in tempMeassure:
            collumnBd = self.collumnBdRelation['Temperatura-Externa'][i]
            data = self.dataGraph(
                startDate, endDate, f'{i}_totais', collumnBd
            )
            dTS = self.graph('Temperatura-Externa', i, data)
            dataSets.append(dTS)

        context = {
            'dataSets': dataSets,
            'labels': labels,
            'graphType': graphType
        }
        return self.template_name, context

    def graphPost(self, request):
        try:
            dataReq = request.POST
            dateStart = dataReq['date-start']
            dateEnd = dataReq['date-end']
            if not dateStart or not dateEnd:
                return self.template_error, {
                    'alert': 'Talves você esqueceu as datas ...'
                }
            if 'flexRadioDefault' in dataReq:
                physQuantity = dataReq['flexRadioDefault']
            else:
                return self.template_error, {
                    'alert': 'Marque um sensor ...'
                }
            dataSets: list = []
            labels: list = self.labelGraph(dateStart, dateEnd)
            for i in self.meassures:
                if i in dataReq:
                    collumnBd = self.collumnBdRelation[physQuantity][i]
                    data = self.dataGraph(
                        dateStart, dateEnd, f'{i}_totais', collumnBd
                    )
                    dTS = self.graph(physQuantity, i, data)
                    dataSets.append(dTS)
            graphTitle = f'De {dateStart} até {dateEnd} : {physQuantity}'
            context = {
                'dataSets': dataSets,
                'labels': labels,
                'graphTitle': graphTitle
            }
            return self.template_name, context
        except Exception as e:
            print(e.__class__.__name__, e)
            return self.template_error, {
                'alert': e,
            }


class TablesView(Queries):
    template_error = 'notfound/404.html'

    def tableGet(self, request, numberPager: int):
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
        except Exception as e:
            return (self.template_error, {'alert': e})

    def tablePost(self, request, viewBdType: str):
        try:
            recept = request.POST
            dateStart = recept['date-start']
            dateEnd = recept['date-end']
            if not dateStart or not dateEnd:
                return (self.template_error, {
                    'alert': 'Talves você esqueceu as datas ...'}
                )
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


class PagesTableMeanView(View, TablesView):
    template_name = 'registros/tabela/meantable.html'
    action_url = "/registros/tabela/medias"
    checkDict: dict = {
        'umi': 1,
        'press': 1,
        't1': 1,
        't2': 1,
    }

    def get(self, request):
        template, context = self.tableGet(request, 30)
        return render(request, template, context)

    def post(self, request):
        template, context = self.tablePost(request, 'medias')
        return render(request, template, context)


class PagesTablesMaxView(View, TablesView):
    template_name = 'registros/tabela/maxtable.html'
    action_url = "/registros/tabela/maximos"
    checkDict: dict = {
        'umi': 1,
        'press': 1,
        't1': 1,
        't2': 1,
    }

    def get(self, request):
        template, context = self.tableGet(request, 30)
        return render(request, template, context)

    def post(self, request):
        template, context = self.tablePost(request, 'maximas')
        return render(request, template, context)


class PagesTablesMinView(View, TablesView):
    template_name = 'registros/tabela/mintable.html'
    action_url = "/registros/tabela/minimos"
    checkDict: dict = {
        'umi': 1,
        'press': 1,
        't1': 1,
        't2': 1,
    }

    def get(self, request):
        template, context = self.tableGet(request, 30)
        return render(request, template, context)

    def post(self, request):
        template, context = self.tablePost(request, 'minimas')
        return render(request, template, context)


class PagesTablesMedianView(View, TablesView):
    template_name = 'registros/tabela/mediantable.html'
    action_url = "/registros/tabela/medianas"
    checkDict: dict = {
        'umi': 1,
        'press': 1,
        't1': 1,
        't2': 1,
    }

    def get(self, request):
        template, context = self.tableGet(request, 30)
        return render(request, template, context)

    def post(self, request):
        template, context = self.tablePost(request, 'medianas')
        return render(request, template, context)


class PagesTablesModeView(View, TablesView):
    template_name = 'registros/tabela/modetable.html'
    action_url = "/registros/tabela/modas"
    checkDict: dict = {
        'umi': 1,
        'press': 1,
        't1': 1,
        't2': 1,
    }

    def get(self, request):
        template, context = self.tableGet(request, 30)
        return render(request, template, context)

    def post(self, request):
        template, context = self.tablePost(request, 'modas')
        return render(request, template, context)


class PagesGraphsViewBar(View, GraphsView):
    template_name = 'registros/graficos/bargraphs.html'
    action_url = '/registros/graficos/barra'
    graphType = 'Gráfico de Barras - Temperatura dos Últimos 5 dias.'

    def get(self, request):
        template_name, context = self.graphGet(request, self.graphType)
        return render(request, template_name, context)

    def post(self, request):
        template_name, context = self.graphPost(request)
        return render(request, template_name, context)


class PagesGraphsViewLine(View, GraphsView):
    template_name = 'registros/graficos/linegraphs.html'
    action_url = '/registros/graficos/linha'
    graphType = 'Gráfico de Linhas - Temperatura dos Últimos 5 dias.'

    def get(self, request):
        template_name, context = self.graphGet(request, self.graphType)
        return render(request, template_name, context)

    def post(self, request):
        template_name, context = self.graphPost(request)
        return render(request, template_name, context)


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
