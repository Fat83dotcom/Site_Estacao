# Generated by Django 4.2.1 on 2023-09-02 12:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Core', '0006_totalmax_totalmeans'),
    ]

    operations = [
        migrations.CreateModel(
            name='TotalMin',
            fields=[
                ('codigo', models.BigIntegerField(primary_key=True, serialize=False)),
                ('dia', models.DateField()),
                ('minimo_umidade', models.FloatField()),
                ('minimo_pressao', models.FloatField()),
                ('minimo_temp_int', models.FloatField()),
                ('minimo_temp_ext', models.FloatField()),
            ],
            options={
                'db_table': 'minimas_totais',
                'managed': False,
            },
        ),
    ]
