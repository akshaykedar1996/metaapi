from django.contrib import admin
from .models import *
# Register your models here.
@admin.register(SubAdminDT)
class ProductAdmin(admin.ModelAdmin):
   
    list_display = [field.name for field in SubAdminDT._meta.fields]   