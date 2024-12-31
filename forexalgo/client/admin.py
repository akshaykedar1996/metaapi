from django.contrib import admin
from .models import *
# Register your models here.
@admin.register(ClientDetail)
class ProductAdmin(admin.ModelAdmin):
   
    list_display = [field.name for field in ClientDetail._meta.fields]   


@admin.register(SYMBOL)
class ProductAdmin(admin.ModelAdmin):
   
    list_display = [field.name for field in SYMBOL._meta.fields]      



@admin.register(GROUP)
class ProductAdmin(admin.ModelAdmin):
   
    list_display = [field.name for field in GROUP._meta.fields]   

@admin.register(ClientSignal)
class ProductAdmin(admin.ModelAdmin):
   
    list_display = [field.name for field in ClientSignal._meta.fields]       


@admin.register(Client_SYMBOL_QTY)
class ProductAdmin(admin.ModelAdmin):
   
    list_display = [field.name for field in Client_SYMBOL_QTY._meta.fields]            