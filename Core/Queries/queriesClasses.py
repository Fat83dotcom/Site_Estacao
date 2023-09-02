from pytz import timezone
from datetime import datetime, timedelta


class DateManager:
    def formatDate(self, format: str, datetimeObj: datetime):
        return datetimeObj.strftime(format)

    def currentYear(self):
        dateToday = str(datetime.now(timezone('America/Sao_Paulo')))
        dateToday = datetime.strptime(
            dateToday, '%Y-%m-%d %H:%M:%S.%f%z'
        )
        currentYear: str = dateToday.strftime('%Y')
        return currentYear

    def _dateYesterday(self):
        dateToday = str(datetime.now(timezone('America/Sao_Paulo')))
        dateYesterday = datetime.strptime(
            dateToday, '%Y-%m-%d %H:%M:%S.%f%z'
        ) - timedelta(1)
        queryDate = dateYesterday.strftime('%Y-%m-%d')
        return queryDate

    def _retroactiveDate(self, numberDaysTurnBack: int):
        dateToday = str(datetime.now(timezone('America/Sao_Paulo')))
        dateYesterday = datetime.strptime(
            dateToday, '%Y-%m-%d %H:%M:%S.%f%z'
        ) - timedelta(numberDaysTurnBack)
        queryDate = dateYesterday.strftime('%Y-%m-%d')
        return queryDate

    def systemFormatDateToday(self) -> str:
        dateToday = datetime.now(timezone('America/Sao_Paulo'))
        return dateToday.strftime('%d-%m-%Y')

    def systemFormatDateYesterday(self) -> str:
        dateToday = datetime.now(timezone('America/Sao_Paulo'))
        dateYesterday = dateToday - timedelta(1)
        return dateYesterday.strftime('%d-%m-%Y')


class Queries(DateManager):
    def queryDateYesterday(self) -> tuple:
        sql = 'SELECT * FROM dado_diario WHERE dia=%s'
        data: tuple = (f"{self._dateYesterday()} 00:00:00", )
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
        sql = f'SELECT codigo, {collumn} ' \
            f'FROM {viewBdType} WHERE dia BETWEEN %s AND %s' \
            f' ORDER BY dia {ordering}'
        data: tuple = (dateStart, dateEnd)
        return (sql, data)

    def queryFilterMaxByCurrentYear(
        self, collumn: str, ordering='DESC'
    ) -> tuple:
        currentYear = str(self.currentYear())
        sql = f'SELECT codigo, dia, {collumn} FROM dado_diario' \
            f' WHERE {collumn}=' \
            f'(SELECT MAX({collumn}) ' \
            f'FROM dado_diario WHERE EXTRACT(YEAR FROM(SELECT dia))=%s) AND' \
            f' EXTRACT(YEAR FROM(SELECT dia))=%s ORDER BY dia {ordering}'
        data: tuple = (currentYear, currentYear)
        return (sql, data)

    def queryFilterMinByCurrentYear(
        self, collumn: str, ordering='DESC'
    ) -> tuple:
        currentYear = str(self.currentYear())
        sql = f'SELECT codigo, dia, {collumn} FROM dado_diario' \
            f' WHERE {collumn}=' \
            f'(SELECT MIN({collumn}) ' \
            f'FROM dado_diario WHERE EXTRACT(YEAR FROM(SELECT dia))=%s) AND' \
            f' EXTRACT(YEAR FROM(SELECT dia))=%s ORDER BY dia {ordering}'
        data: tuple = (currentYear, currentYear)
        return (sql, data)

    def queryFilterMeanByCurrentYear(self, collumn: str) -> tuple:
        currentYear = self.currentYear()
        sql = f'SELECT 1 AS codigo, AVG({collumn}) FROM' \
            ' dado_diario WHERE EXTRACT(YEAR FROM(SELECT dia))=%s'
        data: tuple = (currentYear, )
        return (sql, data)

    def queryFilterMeanByYear(self, year: str, collumn: str) -> tuple:
        sql = f'SELECT 1 AS codigo, AVG({collumn}) FROM' \
            ' dado_diario WHERE EXTRACT(YEAR FROM(SELECT dia))=%s'
        data: tuple = (year, )
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

    def queryExtractYearsFromTable(self) -> tuple:
        sql = 'SELECT DISTINCT EXTRACT(YEAR FROM dia) as ano, 1 as codigo ' \
            'FROM dado_diario'
        data: tuple = ()
        return sql, data

    def queryFilterMeassureByYear(
            self, year: str,
            collumn: str,
            functionSQL: str,
            ordering: str) -> tuple:
        sql = f'SELECT codigo, dia, {collumn} FROM dado_diario' \
            f' WHERE {collumn}=' \
            f'(SELECT {functionSQL}({collumn}) ' \
            'FROM dado_diario WHERE EXTRACT(YEAR FROM(SELECT dia))=%s) AND' \
            f' EXTRACT(YEAR FROM(SELECT dia))=%s ORDER BY dia {ordering}'
        data = (year, year)
        return sql, data

    def query3LastDays(self) -> tuple:
        dateYesterday = self._retroactiveDate(1)
        dayBeforeYesterday = self._retroactiveDate(2)
        oneDayBeforeYesterday = self._retroactiveDate(3)

        sql = f'''
        SELECT
            *
        FROM
            "tabelas_horarias"."{dateYesterday}"
        WHERE
            (EXTRACT(MINUTE FROM data_hora)=0
            OR
            EXTRACT(MINUTE FROM data_hora)=30)
            AND
            EXTRACT(Second FROM data_hora)=0
        union
        SELECT
            *
        FROM
            "tabelas_horarias"."{dayBeforeYesterday}"
        WHERE
            (EXTRACT(MINUTE FROM data_hora)=0
            OR
            EXTRACT(MINUTE FROM data_hora)=30)
            AND
            EXTRACT(Second FROM data_hora)=0
            union
        SELECT
            *
        FROM
            "tabelas_horarias"."{oneDayBeforeYesterday}"
        WHERE
            (EXTRACT(MINUTE FROM data_hora)=0
            OR
            EXTRACT(MINUTE FROM data_hora)=30)
            AND
            EXTRACT(Second FROM data_hora)=0
        OREDER BY data_hora ASC
        '''
        data = ()
        return sql, data

    def queryMean3LastDays(self) -> tuple:
        pass

    def queryLastDailyEntry(self) -> tuple:
        tableName = self.systemFormatDateToday()
        sql = f'''
        SELECT * FROM gerenciador_tabelas_horarias
        INNER JOIN "tabelas_horarias"."{tableName}"
        ON gerenciador_tabelas_horarias.codigo=
        "tabelas_horarias"."{tableName}".codigo_gerenciador
        ORDER BY "tabelas_horarias"."{tableName}".codigo DESC LIMIT 1
        '''
        data = ()
        return sql, data

    def queryLast24Hours(self) -> tuple:
        tableNameToday = self.systemFormatDateToday()
        tableNameYesterday = self.systemFormatDateYesterday()
        sql = f'''
        SELECT * FROM gerenciador_tabelas_horarias
        INNER JOIN "tabelas_horarias"."{tableNameToday}"
        ON gerenciador_tabelas_horarias.codigo=
        "tabelas_horarias"."{tableNameToday}".codigo_gerenciador
        WHERE data_hora <= clock_timestamp()
            AND EXTRACT(SECOND FROM data_hora) = 0
            AND (EXTRACT(MINUTE FROM data_hora) %% 5 = 0)
        UNION
        SELECT * FROM gerenciador_tabelas_horarias
        INNER JOIN "tabelas_horarias"."{tableNameYesterday}"
        ON gerenciador_tabelas_horarias.codigo=
        "tabelas_horarias"."{tableNameYesterday}".codigo_gerenciador
        WHERE data_hora >= (clock_timestamp() - INTERVAL '27 hours')
            AND EXTRACT(SECOND FROM data_hora) = 0
            AND (EXTRACT(MINUTE FROM data_hora) %% 5 = 0)
        ORDER BY data_hora;
        '''
        data = ()
        return sql, data
