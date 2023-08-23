import locale
from rest_framework import serializers
from rest_framework.response import Response
from rest_framework.decorators import api_view
from Core.Queries.queriesClasses import Queries
from Core.models import GerenciadorTabelasHorarias
locale.setlocale(locale.LC_TIME, 'pt_BR.utf8')


class DailyEntrySerializer(serializers.Serializer):
    data_hora = serializers.DateField()
    umidade = serializers.FloatField()
    pressao = serializers.FloatField()
    temp_int = serializers.FloatField()
    temp_ext = serializers.FloatField()


@api_view()
def lastDailyEntry(request):
    q = Queries()
    sql, data = q.queryLastDailyEntry()
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
        for i in GerenciadorTabelasHorarias.objects.raw(sql, data)
    ]
    serializer = DailyEntrySerializer(instance=result[0])
    return Response(serializer.data)


@api_view()
def last24HoursEntry(request):
    q = Queries()
    sql, data = q.queryLast24Hours()
    result = [
        {
            'data_hora': str(i.data_hora.strftime("%d/%m %H:%M")),
            'umidade': float(i.umidade),
            'pressao': float(i.pressao),
            'temp_int': float(i.temp_int),
            'temp_ext': float(i.temp_ext)
        }
        for i in GerenciadorTabelasHorarias.objects.raw(sql, data)
    ]
    serializer = DailyEntrySerializer(instance=result, many=True)
    return Response(serializer.data)
