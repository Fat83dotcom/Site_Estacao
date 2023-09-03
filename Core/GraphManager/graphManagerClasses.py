from Core.models import DateLabel, GenericViews
from Core.Queries.queriesClasses import Queries


class ManagerGraphs(Queries):
    colors = {
        'Umidade': {
            'maximas': 'rgba(92, 88, 11, 0.6)',
            'minimas': 'rgba(232, 222, 28, 0.6)',
            'medias': 'rgba(219, 211, 27, 0.6)',
            'medianas': 'rgba(156, 149, 19, 0.6)',
            'modas': 'rgba(194, 185, 23, 0.6)',
            'unity': '%',
        },
        'Pressao': {
            'maximas': 'rgba(22, 92, 50, 0.6)',
            'minimas': 'rgba(56, 232, 126, 0.6)',
            'medias': 'rgba(37, 156, 85, 0.6)',
            'medianas': 'rgba(53, 219, 119, 0.6)',
            'modas': 'rgba(47, 194, 105, 0.6)',
            'unity': 'hPa',
        },
        'Temperatura-Interna': {
            'maximas': 'rgba(36, 34, 92, 0.6)',
            'minimas': 'rgba(91, 86, 232, 0.6)',
            'medias': 'rgba(61, 58, 156, 0.6)',
            'medianas': 'rgba(86, 82, 219, 0.6)',
            'modas': 'rgba(76, 72, 194, 0.6)',
            'unity': '°C',
        },
        'Temperatura-Externa': {
            'maximas': 'rgba(92, 17, 13, 0.6',
            'minimas': 'rgba(232, 42, 32, 0.6)',
            'medias': 'rgba(156, 28, 22, 0.6)',
            'medianas': 'rgba(220, 41, 31, 0.6)',
            'modas': 'rgba(194, 35, 27, 0.6)',
            'unity': '°C',
        }
    }
    collumnBdRelation = {
        'Umidade': {
            'medias': 'umidade',
            'maximas': 'umidade',
            'minimas': 'umidade',
            'medianas': 'umidade',
            'modas': 'umidade'
        },
        'Pressao': {
            'medias': 'pressao',
            'maximas': 'pressao',
            'minimas': 'pressao',
            'medianas': 'pressao',
            'modas': 'pressao'
        },
        'Temperatura-Interna': {
            'medias': 'temp_int',
            'maximas': 'temp_int',
            'minimas': 'temp_int',
            'medianas': 'temp_int',
            'modas': 'temp_int'
        },
        'Temperatura-Externa': {
            'medias': 'temp_ext',
            'maximas': 'temp_ext',
            'minimas': 'temp_ext',
            'medianas': 'temp_ext',
            'modas': 'temp_ext'
        },
    }
    meassures = ['medias', 'maximas', 'minimas', 'medianas', 'modas']
    dataReqGet = ['maximas', 'minimas', 'medias']
    physQuantityGet = 'Temperatura-Externa'

    def graph(self, physQuantity: str, meassure: str, data: list) -> dict:
        returnDataSet = {
            'label': f'{physQuantity} - {meassure}',
            'data': data,
            'backgroundColor': self.colors[physQuantity][meassure],
            'borderColor': '#000',
            'borderWidth': 0.5,
            'fill': 'origin',
            'pointRadius': 1.5,
            'cubicInterpolationMode': 'monotone',
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
            result = GenericViews.queryGenericViews(
                viewBdType, dateStart, dateEnd
            )
            for i in result:
                collumnValue = getattr(i, collumnBd)
                extractData.append(collumnValue)
            return extractData
        except Exception as e:
            raise e

    def buildLabelGraph(self, dateStart: str, dateEnd: str) -> list:
        label: list = []
        result = DateLabel.objects.filter(
            dia__range=(dateStart, dateEnd)
        ).order_by('dia')
        for i in result:
            date = self.formatDate('%d/%m/%Y', i.dia)
            label.append(date)
        return label

    def buildDataSet(
        self, startDate, endDate, request, physQuantity
    ) -> list:
        dataSets: list = []
        for i in self.meassures:
            if i in request:
                collumnBd = self.collumnBdRelation[physQuantity][i]
                data = self.dataGraph(
                    startDate, endDate, f'{i}_totais', collumnBd
                )
                dTS = self.graph(physQuantity, i, data)
                dataSets.append(dTS)
        return dataSets


class GraphsView(ManagerGraphs):
    template_error = 'notfound/404.html'
    nDaysTurnBack = 30

    def graphGet(self, graphName: str, numberDaysTurnBack: int):
        startDate = self._retroactiveDate(numberDaysTurnBack)
        endDate = self._retroactiveDate(1)
        labels: list = self.buildLabelGraph(startDate, endDate)
        dataSets: list = self.buildDataSet(
            startDate, endDate, self.dataReqGet, self.physQuantityGet
        )
        graphType = f'Gráfico de {graphName} - ' + \
            f'Temperatura dos Últimos {numberDaysTurnBack} dias.'
        context = {
            'dataSets': dataSets,
            'labels': labels,
            'graphType': graphType,
            'unity': self.colors[self.physQuantityGet]["unity"]
        }
        return self.template_name, context

    def graphPost(self, request):
        try:
            dataReq = request.POST
            dateStart: str = dataReq['date-start']
            dateEnd: str = dataReq['date-end']
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
            dataSets: list = self.buildDataSet(
                dateStart, dateEnd, dataReq, physQuantity
            )
            labels: list = self.buildLabelGraph(dateStart, dateEnd)
            graphTitle = f'De {dateStart} até {dateEnd} : ' \
                f'{physQuantity} {self.colors[physQuantity]["unity"]}'
            context = {
                'dataSets': dataSets,
                'labels': labels,
                'graphTitle': graphTitle,
                'unity': self.colors[physQuantity]["unity"]
            }
            return self.template_name, context
        except Exception as e:
            print(e.__class__.__name__, e)
            return self.template_error, {
                'alert': e,
            }
