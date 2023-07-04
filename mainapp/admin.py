from django.contrib import admin
from .models import *

# class HistoyrAdmin(admin.ModelAdmin):
#     list_display = ('user','image','action')

admin.site.register((
    Image,
    History,
    Profile,
    ))
# admin.site.register(History,HistoyrAdmin)