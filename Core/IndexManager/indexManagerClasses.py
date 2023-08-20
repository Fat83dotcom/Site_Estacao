from Core.models import DadoDiario
from Core.Queries.queriesClasses import Queries
from Core.GraphManager.graphManagerClasses import ManagerGraphs


class IndexEstatisticsManager(Queries):
    def extractYears(self) -> list:
        sql, data = self.queryExtractYearsFromTable()
        result = DadoDiario.objects.raw(sql, data)
        year: list = [str(y.ano) for y in result]
        return year

    def templateData(self, year) -> dict:
        try:
            sql, data = self.queryFilterMeassureByYear(
                year,
                'maximo_temp_ext',
                'MAX',
                'DESC'
            )
            resultMaxTemp = DadoDiario.objects.raw(sql, data)

            sql, data = self.queryFilterMeassureByYear(
                year,
                'minimo_temp_ext',
                'MIN',
                'DESC'
            )
            resultMinTemp = DadoDiario.objects.raw(sql, data)
            sql, data = self.queryFilterMeanByYear(year, 'media_temp_ext')
            resultMeanTemp = DadoDiario.objects.raw(sql, data)
            sql, data = self.queryFilterMeassureByYear(
                year,
                'maximo_umidade',
                'MAX',
                'DESC'
            )
            resultMaxUmi = DadoDiario.objects.raw(sql, data)
            sql, data = self.queryFilterMeassureByYear(
                year,
                'minimo_umidade',
                'MIN',
                'DESC'
            )
            resultMinUmi = DadoDiario.objects.raw(sql, data)
            sql, data = self.queryFilterMeanByYear(year, 'media_umidade')
            resultMeanUmi = DadoDiario.objects.raw(sql, data)
            sql, data = self.queryFilterMeassureByYear(
                year,
                'maximo_pressao',
                'MAX',
                'ASC'
            )
            resultMaxPress = DadoDiario.objects.raw(sql, data)
            sql, data = self.queryFilterMeassureByYear(
                year,
                'minimo_pressao',
                'MIN',
                'DESC'
            )
            resultMinPress = DadoDiario.objects.raw(sql, data)
            sql, data = self.queryFilterMeanByYear(year, 'media_pressao')
            resultMeanPress = DadoDiario.objects.raw(sql, data)
            result = {
                'year': year,
                'resultMaxTemp': resultMaxTemp,
                'resultMinTemp': resultMinTemp,
                'resultMeanTemp': resultMeanTemp,
                'resultMaxUmi': resultMaxUmi,
                'resultMinUmi': resultMinUmi,
                'resultMeanUmi': resultMeanUmi,
                'resultMaxPress': resultMaxPress,
                'resultMinPress': resultMinPress,
                'resultMeanPress': resultMeanPress,
            }
            return result
        except Exception as e:
            raise e


class IndexGraphManager(ManagerGraphs):
    pass
