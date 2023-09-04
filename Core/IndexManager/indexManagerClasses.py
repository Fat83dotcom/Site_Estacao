from Core.models import DadoDiario
from Core.GraphManager.graphManagerClasses import ManagerGraphs


class IndexEstatisticsManager:
    def extractYears(self) -> list:
        result = DadoDiario.extractYear()
        year: list = [str(y.get('year', 0)) for y in result]
        return year

    def templateData(self, year) -> dict:
        try:
            resultMaxTemp = DadoDiario.queryFilterMeassureByYear(
                year,
                'maximo_temp_ext',
                'MAX',
                'DESC'
            )
            resultMinTemp = DadoDiario.queryFilterMeassureByYear(
                year,
                'minimo_temp_ext',
                'MIN',
                'DESC'
            )
            resultMeanTemp = DadoDiario.queryFilterMeanByYear(
                year, 'media_temp_ext'
            )
            resultMaxUmi = DadoDiario.queryFilterMeassureByYear(
                year,
                'maximo_umidade',
                'MAX',
                'DESC'
            )
            resultMinUmi = DadoDiario.queryFilterMeassureByYear(
                year,
                'minimo_umidade',
                'MIN',
                'DESC'
            )
            resultMeanUmi = DadoDiario.queryFilterMeanByYear(
                year, 'media_umidade'
            )
            resultMaxPress = DadoDiario.queryFilterMeassureByYear(
                year,
                'maximo_pressao',
                'MAX',
                'ASC'
            )
            resultMinPress = DadoDiario.queryFilterMeassureByYear(
                year,
                'minimo_pressao',
                'MIN',
                'DESC'
            )
            resultMeanPress = DadoDiario.queryFilterMeanByYear(
                year, 'media_pressao'
            )
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
