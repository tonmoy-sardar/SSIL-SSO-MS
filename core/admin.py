from django.contrib import admin
from core.models import *

@admin.register(TCorePermissions)
class TCorePermissions(admin.ModelAdmin):
    list_display = [field.name for field in TCorePermissions._meta.fields]

@admin.register(TCoreRole)
class TCoreRole(admin.ModelAdmin):
    list_display = [field.name for field in TCoreRole._meta.fields]

# @admin.register(TCoreFunctionalArea)
# class TCoreFunctionalArea(admin.ModelAdmin):
#     list_display = [field.name for field in TCoreFunctionalArea._meta.fields]


# @admin.register(TCoreLogicalAreas)
# class TCoreLogicalAreas(admin.ModelAdmin):
#     list_display = [field.name for field in TCoreLogicalAreas._meta.fields]

@admin.register(TCoreModule)
class TCoreModule(admin.ModelAdmin):
    list_display = [field.name for field in TCoreModule._meta.fields]


# @admin.register(TCoreOther)
# class TCoreOther(admin.ModelAdmin):
#     list_display = [field.name for field in TCoreOther._meta.fields]

@admin.register(TCoreUnit)
class TCoreUnit(admin.ModelAdmin):
    list_display = [field.name for field in TCoreUnit._meta.fields]