# Generated by Django 4.2.1 on 2023-09-02 14:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Core', '0009_totalmode'),
    ]

    operations = [
        migrations.CreateModel(
            name='GenericViews',
            fields=[
                ('codigo', models.BigIntegerField(primary_key=True, serialize=False)),
                ('dia', models.DateField()),
                ('umidade', models.FloatField()),
                ('pressao', models.FloatField()),
                ('temp_int', models.FloatField()),
                ('temp_ext', models.FloatField()),
            ],
        ),
    ]
