from django.contrib import admin

from master.models import *

@admin.register(TMasterModuleRole)
class TMasterModuleRole(admin.ModelAdmin):
    list_display = [field.name for field in TMasterModuleRole._meta.fields]
    search_fields = ('mmr_module__id', 'mmr_user__username')

@admin.register(TMasterModuleGroup)
class TMasterModuleGroup(admin.ModelAdmin):
    list_display = [field.name for field in TMasterModuleGroup._meta.fields]