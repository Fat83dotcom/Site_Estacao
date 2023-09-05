import locale
from rest_framework import serializers
from rest_framework.views import APIView
from rest_framework.response import Response
from Core.models import DataFromTabelasHorarias
from Core.Queries.queriesClasses import DateManager
locale.setlocale(locale.LC_TIME, 'pt_BR.utf8')


class DailyEntrySerializer(serializers.Serializer):
    data_hora = serializers.DateField()
    umidade = serializers.FloatField()
    pressao = serializers.FloatField()
    temp_int = serializers.FloatField()
    temp_ext = serializers.FloatField()


class LastEntry(APIView):
    def get(self, request):
        tableName = DateManager.systemFormatDateToday()
        result = [
            {
                'data_hora': str(
                    i.data_hora.strftime("%A, %d/%m/%Y %H:%M:%S").title()
                ),
                'umidade': float(i.umidade),
                'pressao': float(i.pressao),
                'temp_int': float(i.temp_int),
                'temp_ext': float(i.temp_ext)
            }
            for i in DataFromTabelasHorarias.getLastEntry(tableName)
        ]
        serializer = DailyEntrySerializer(instance=result[0])
        return Response(serializer.data)


class Last24HoursEntry(APIView):
    def get(self, request):
        tableNameToday = DateManager.systemFormatDateToday()
        tableNameYesterday = DateManager.systemFormatDateYesterday()
        result = [
            {
                'data_hora': str(i.data_hora.strftime("%d/%m %H:%M")),
                'umidade': float(i.umidade),
                'pressao': float(i.pressao),
                'temp_int': float(i.temp_int),
                'temp_ext': float(i.temp_ext)
            }
            for i in DataFromTabelasHorarias.getLast24Hours(
                tableNameToday, tableNameYesterday
            )
        ]
        serializer = DailyEntrySerializer(instance=result, many=True)
        return Response(serializer.data)
