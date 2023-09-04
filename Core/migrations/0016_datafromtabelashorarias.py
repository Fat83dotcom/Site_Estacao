# Generated by Django 4.2.1 on 2023-09-03 17:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Core', '0015_alter_genericviews_table'),
    ]

    operations = [
        migrations.CreateModel(
            name='DataFromTabelasHorarias',
            fields=[
                ('codigo', models.IntegerField(primary_key=True, serialize=False)),
                ('data_hora', models.DateField()),
                ('umidade', models.FloatField()),
                ('pressao', models.FloatField()),
                ('temp_int', models.FloatField()),
                ('temp_ext', models.FloatField()),
            ],
            options={
                'db_table': 'get_last_24_hours',
                'managed': False,
            },
        ),
    ]