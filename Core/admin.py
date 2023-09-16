from django.contrib import admin
from .models import DadoDiario, Pictures, FavPicture


@admin.register(DadoDiario)
class DadoDiarioAdmin(admin.ModelAdmin):
    ...


@admin.register(Pictures)
class PicturesAdmin(admin.ModelAdmin):
    ...


@admin.register(FavPicture)
class FavPictureAdmin(admin.ModelAdmin):
    list_display = 'name', 'favIcon'
