from django.views import View
from Core.Queries.queriesClasses import Queries
from Core.GraphManager.graphManagerClasses import GraphsView
from Core.IndexManager.indexManagerClasses import IndexEstatisticsManager
from django.shortcuts import render
from Core.models import DadoDiario, Pictures, TotalMeans, TotalMax
from Core.models import TotalMedian, TotalMode, TotalMin, GenericViews
from django.core.paginator import Paginator


class TablesView(Queries):
    template_error = 'notfound/404.html'

    def tableGet(self, request, numberPager: int, query):
        try:
            result = query
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
    pageName = 'Médias'
    checkDict: dict = {
        'umi': 1,
        'press': 1,
        't1': 1,
        't2': 1,
    }

    def get(self, request):
        template, context = self.tableGet(request, 30)
        context.update({'pageName': self.pageName})
        return render(request, template, context)

    def post(self, request):
        template, context = self.tablePost(request, 'medias')
        context.update({'pageName': self.pageName})
        return render(request, template, context)


class PagesTablesMaxView(View, TablesView):
    template_name = 'registros/tabela/maxtable.html'
    action_url = "/registros/tabela/maximos"
    pageName = 'Máximas'
    checkDict: dict = {
        'umi': 1,
        'press': 1,
        't1': 1,
        't2': 1,
    }

    def get(self, request):
        template, context = self.tableGet(request, 30)
        context.update({'pageName': self.pageName})
        return render(request, template, context)

    def post(self, request):
        template, context = self.tablePost(request, 'maximas')
        context.update({'pageName': self.pageName})
        return render(request, template, context)


class PagesTablesMinView(View, TablesView):
    template_name = 'registros/tabela/mintable.html'
    action_url = "/registros/tabela/minimos"
    pageName = 'Mínimas'
    checkDict: dict = {
        'umi': 1,
        'press': 1,
        't1': 1,
        't2': 1,
    }

    def get(self, request):
        template, context = self.tableGet(request, 30)
        context.update({'pageName': self.pageName})
        return render(request, template, context)

    def post(self, request):
        template, context = self.tablePost(request, 'minimas')
        context.update({'pageName': self.pageName})
        return render(request, template, context)


class PagesTablesMedianView(View, TablesView):
    template_name = 'registros/tabela/mediantable.html'
    action_url = "/registros/tabela/medianas"
    pageName = 'Medianas'
    checkDict: dict = {
        'umi': 1,
        'press': 1,
        't1': 1,
        't2': 1,
    }

    def get(self, request):
        template, context = self.tableGet(request, 30)
        context.update({'pageName': self.pageName})
        return render(request, template, context)

    def post(self, request):
        template, context = self.tablePost(request, 'medianas')
        context.update({'pageName': self.pageName})
        return render(request, template, context)


class PagesTablesModeView(View, TablesView):
    template_name = 'registros/tabela/modetable.html'
    action_url = "/registros/tabela/modas"
    pageName = 'Modas'
    checkDict: dict = {
        'umi': 1,
        'press': 1,
        't1': 1,
        't2': 1,
    }

    def get(self, request):
        template, context = self.tableGet(request, 30)
        context.update({'pageName': self.pageName})
        return render(request, template, context)

    def post(self, request):
        template, context = self.tablePost(request, 'modas')
        context.update({'pageName': self.pageName})
        return render(request, template, context)


class PagesGraphsViewBar(View, GraphsView):
    template_name = 'registros/graficos/bargraphs.html'
    action_url = '/registros/graficos/barra'
    pageName = 'Gráfico de '

    def get(self, request, graphName):
        template_name, context = self.graphGet(
            graphName,
            self.nDaysTurnBack
        )
        context.update({'pageName': f'{self.pageName}{graphName}'})
        return render(request, template_name, context)

    def post(self, request, graphName):
        template_name, context = self.graphPost(request)
        context.update({'pageName': f'{self.pageName}{graphName}'})
        return render(request, template_name, context)


class PagesGraphsViewLine(View, GraphsView):
    template_name = 'registros/graficos/linegraphs.html'
    action_url = '/registros/graficos/linha'
    pageName = 'Gráfico de '

    def get(self, request, graphName):
        template_name, context = self.graphGet(
            graphName,
            self.nDaysTurnBack
        )
        context.update({'pageName': f'{self.pageName}{graphName}'})
        return render(request, template_name, context)

    def post(self, request, graphName):
        template_name, context = self.graphPost(request)
        context.update({'pageName': f'{self.pageName}{graphName}'})
        return render(request, template_name, context)


class PageIndexView(View, IndexEstatisticsManager):
    template_name = 'index/index.html'
    template_error = 'notfound/404.html'
    pageName = 'BrainStorm Tecnologia'

    def get(self, request):
        try:
            years = self.extractYears()
            context = {
                'years': years,
                'data': []
            }
            for year in years:
                context['data'].append(self.templateData(year))
            context.update({'pageName': self.pageName})
            return render(request, self.template_name, context)
        except Exception as e:
            print(e.__class__.__name__, e)
            return render(request, self.template_error)


class PageAboutView(View):
    template_name = 'sobre/sobre.html'
    template_error = 'notfound/404.html'
    pageName = 'Sobre'

    def get(self, request):
        try:
            pic = Pictures.objects.all()
            context = {'pic': pic, }
            context.update({'pageName': self.pageName})
            return render(request, self.template_name, context)
        except Exception:
            return render(request, self.template_error)


class PageMainRegisters(View, Queries):
    template_name = 'registros/menuRegistros.html'
    template_error = 'notfound/404.html'
    pageName = 'Registros'

    def get(self, request):
        try:
            query, data = self.queryDateYesterday()
            dateToday = DadoDiario.objects.raw(query, data)
            context = {
                'dateToday': dateToday,
            }
            context.update({'pageName': self.pageName})
            return render(request, self.template_name, context)
        except Exception:
            return render(request, self.template_error)

    def post(self, request):
        context = {}
        context.update({'pageName': self.pageName})
        return render(request, self.template_error, context)


class PageMainTables(View):
    template_name = 'registros/tabela/tabela.html'
    template_error = 'notfound/404.html'
    pageName = 'Tabelas'

    def get(self, request):
        context = {}
        context.update({'pageName': self.pageName})
        return render(request, self.template_name, context)

    def post(self, request):
        context = {}
        context.update({'pageName': self.pageName})
        return render(request, self.template_error, context)


class PageMainGraphs(View):
    template_name = 'registros/graficos/grafico.html'
    template_error = 'notfound/404.html'
    pageName = 'Gráficos'

    def get(self, request):
        context = {}
        context.update({'pageName': self.pageName})
        return render(request, self.template_name, context)


class PageError(View):
    template_name = 'notfound/404.html'
    pageName = 'Erro'

    def get(self, request):
        context = {}
        context.update({'pageName': self.pageName})
        return render(request, self.template_name, context)
