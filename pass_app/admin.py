from django.contrib import admin

from .models import Barcode, Field, Location, Pass, PassInformation


# Register your models here.
@admin.register(Field)
class FieldAdmin(admin.ModelAdmin):
    search_fields = ("key", 'value', 'label', )
    list_display = ("key", 'value', 'label', )


@admin.register(Barcode)
class BarcodeAdmin(admin.ModelAdmin):
    search_fields = ('message', )
    list_display = ('message', 'format', )


@admin.register(Location)
class LocationAdmin(admin.ModelAdmin):
    search_fields = ('latitude', 'longitude', )


@admin.register(Pass)
class PassAdmin(admin.ModelAdmin):
    search_fields = ('description', 'pk')
    list_display = ('description', 'pk')


@admin.register(PassInformation)
class PassInfoAdmin(admin.ModelAdmin):
    pass
