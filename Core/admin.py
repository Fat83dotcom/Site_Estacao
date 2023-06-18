from django.contrib import admin
from .models import DadoDiario, Pictures


@admin.register(DadoDiario)
class DadoDiarioAdmin(admin.ModelAdmin):
    ...


@admin.register(Pictures)
class PicturesAdmin(admin.ModelAdmin):
    ...
