# Generated by Django 4.2.1 on 2023-06-17 21:17

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='DadoDiario',
            fields=[
                ('codigo', models.AutoField(primary_key=True, serialize=False)),
                ('dia', models.DateTimeField(unique=True)),
                ('media_umidade', models.FloatField()),
                ('minimo_umidade', models.FloatField()),
                ('maximo_umidade', models.FloatField()),
                ('mediana_umidade', models.FloatField()),
                ('moda_umidade', models.FloatField()),
                ('media_pressao', models.FloatField()),
                ('minimo_pressao', models.FloatField()),
                ('maximo_pressao', models.FloatField()),
                ('mediana_pressao', models.FloatField()),
                ('moda_pressao', models.FloatField()),
                ('media_temp_int', models.FloatField()),
                ('minimo_temp_int', models.FloatField()),
                ('maximo_temp_int', models.FloatField()),
                ('mediana_temp_int', models.FloatField()),
                ('moda_temp_int', models.FloatField()),
                ('media_temp_ext', models.FloatField()),
                ('minimo_temp_ext', models.FloatField()),
                ('maximo_temp_ext', models.FloatField()),
                ('mediana_temp_ext', models.FloatField()),
                ('moda_temp_ext', models.FloatField()),
            ],
            options={
                'db_table': 'dado_diario',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='Pictures',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('picture', models.ImageField(upload_to='pic/%Y/%m/%d')),
            ],
        ),
    ]
