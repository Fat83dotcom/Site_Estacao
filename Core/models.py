from django.db import models
from django.db.models.functions import ExtractYear


class DadoDiario(models.Model):
    codigo = models.AutoField(primary_key=True)
    dia = models.DateField(unique=True)
    media_umidade = models.FloatField()
    minimo_umidade = models.FloatField()
    maximo_umidade = models.FloatField()
    mediana_umidade = models.FloatField()
    moda_umidade = models.FloatField()
    media_pressao = models.FloatField()
    minimo_pressao = models.FloatField()
    maximo_pressao = models.FloatField()
    mediana_pressao = models.FloatField()
    moda_pressao = models.FloatField()
    media_temp_int = models.FloatField()
    minimo_temp_int = models.FloatField()
    maximo_temp_int = models.FloatField()
    mediana_temp_int = models.FloatField()
    moda_temp_int = models.FloatField()
    media_temp_ext = models.FloatField()
    minimo_temp_ext = models.FloatField()
    maximo_temp_ext = models.FloatField()
    mediana_temp_ext = models.FloatField()
    moda_temp_ext = models.FloatField()

    class Meta:
        managed = False
        db_table = 'dado_diario'

    def __str__(self):
        return f'{self.dia}'

    @classmethod
    def extractYear(cls):
        return cls.objects.annotate(
            year=ExtractYear('dia')
        ).values('year').distinct()

    @classmethod
    def queryFilterMeanByYear(cls, year: str, collumn: str):
        sql = f'''SELECT 1 AS codigo, AVG({collumn}) FROM
        dado_diario WHERE EXTRACT(YEAR FROM(SELECT dia))={year}'''
        return cls.objects.raw(sql)

    @classmethod
    def queryFilterMeassureByYear(
        cls, year: str, collumn: str, funcSQL: str, ordering: str
    ):
        sql = f'''SELECT codigo, dia, {collumn} FROM dado_diario
            WHERE {collumn}=(SELECT {funcSQL}({collumn})
            FROM dado_diario WHERE EXTRACT(YEAR FROM(SELECT dia))={year}) AND
            EXTRACT(YEAR FROM(SELECT dia))={year} ORDER BY dia {ordering}'''
        return cls.objects.raw(sql)


class Pictures(models.Model):
    name = models.CharField(max_length=20, default='pic')
    picture = models.ImageField(upload_to='pic')

    def __str__(self) -> str:
        return f'{self.name}'


class GerenciadorTabelasHorarias(models.Model):
    codigo = models.AutoField(primary_key=True)
    data_tabela = models.DateField(unique=True)

    class Meta:
        managed = False
        db_table = 'gerenciador_tabelas_horarias'


class DateLabel(models.Model):
    '''View PostgrSQL'''
    codigo = models.BigIntegerField(primary_key=True)
    dia = models.DateField()

    class Meta:
        managed = False
        db_table = 'label_datas'


class TotalMeans(models.Model):
    '''View PostgrSQL'''
    codigo = models.BigIntegerField(primary_key=True)
    dia = models.DateField()
    umidade = models.FloatField()
    pressao = models.FloatField()
    temp_int = models.FloatField()
    temp_ext = models.FloatField()

    class Meta:
        managed = False
        db_table = 'medias_totais'


class TotalMax(models.Model):
    '''View PostgrSQL'''
    codigo = models.BigIntegerField(primary_key=True)
    dia = models.DateField()
    umidade = models.FloatField()
    pressao = models.FloatField()
    temp_int = models.FloatField()
    temp_ext = models.FloatField()

    class Meta:
        managed = False
        db_table = 'maximas_totais'


class TotalMin(models.Model):
    '''View PostgrSQL'''
    codigo = models.BigIntegerField(primary_key=True)
    dia = models.DateField()
    umidade = models.FloatField()
    pressao = models.FloatField()
    temp_int = models.FloatField()
    temp_ext = models.FloatField()

    class Meta:
        managed = False
        db_table = 'minimas_totais'


class TotalMedian(models.Model):
    '''View PostgrSQL'''
    codigo = models.BigIntegerField(primary_key=True)
    dia = models.DateField()
    umidade = models.FloatField()
    pressao = models.FloatField()
    temp_int = models.FloatField()
    temp_ext = models.FloatField()

    class Meta:
        managed = False
        db_table = 'medianas_totais'


class TotalMode(models.Model):
    '''View PostgrSQL'''
    codigo = models.BigIntegerField(primary_key=True)
    dia = models.DateField()
    umidade = models.FloatField()
    pressao = models.FloatField()
    temp_int = models.FloatField()
    temp_ext = models.FloatField()

    class Meta:
        managed = False
        db_table = 'modas_totais'


class GenericViews(models.Model):
    '''Função PostgreSQL'''
    codigo = models.BigIntegerField(primary_key=True)
    dia = models.DateField()
    umidade = models.FloatField()
    pressao = models.FloatField()
    temp_int = models.FloatField()
    temp_ext = models.FloatField()

    @classmethod
    def queryGenericViews(cls, viewBDType: str, dateStart: str, dateEnd: str):
        sql = f'''SELECT * FROM {viewBDType}
            WHERE dia BETWEEN '{dateStart}' AND '{dateEnd}'
            ORDER BY dia ASC'''
        return cls.objects.raw(sql)

    class Meta:
        managed = False
        db_table = 'genericviews'
