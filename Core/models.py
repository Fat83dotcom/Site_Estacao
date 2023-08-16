from django.db import models


class DadoDiario(models.Model):
    codigo = models.AutoField(primary_key=True)
    dia = models.DateTimeField(unique=True)
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
