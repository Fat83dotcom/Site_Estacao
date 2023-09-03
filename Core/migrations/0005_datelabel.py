# Generated by Django 4.2.1 on 2023-09-02 00:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Core', '0004_gerenciadortabelashorarias'),
    ]

    operations = [
        migrations.CreateModel(
            name='DateLabel',
            fields=[
                ('codigo', models.BigIntegerField(primary_key=True, serialize=False)),
                ('dia', models.DateTimeField()),
            ],
            options={
                'db_table': 'label_datas',
                'managed': False,
            },
        ),
    ]