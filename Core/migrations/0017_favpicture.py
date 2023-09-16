# Generated by Django 4.2.1 on 2023-09-16 23:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Core', '0016_datafromtabelashorarias'),
    ]

    operations = [
        migrations.CreateModel(
            name='FavPicture',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(default='pic', max_length=20)),
                ('favIcon', models.ImageField(blank=True, null=True, upload_to='favIcon')),
            ],
        ),
    ]
