from rest_framework.decorators import api_view
from rest_framework.response import Response
from Core.models import GerenciadorTabelasHorarias
from Core.Queries.queriesClasses import Queries
from rest_framework import serializers


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
            'data_hora': str(i.data_hora.strftime("%d/%m/%Y %H:%M:%S")),
            'umidade': float(i.umidade),
            'pressao': float(i.pressao),
            'temp_int': float(i.temp_int),
            'temp_ext': float(i.temp_ext)
        }
        for i in GerenciadorTabelasHorarias.objects.raw(sql, data)
    ]
    serializer = LastDailyEntrySerializer(instance=result[0])
    return Response(serializer.data)
