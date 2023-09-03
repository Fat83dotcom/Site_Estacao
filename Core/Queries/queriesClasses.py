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
