from django.contrib import admin
from users.models import *
# Register your models here.
@admin.register(TCoreUserDetail)
class TCoreUserDetail(admin.ModelAdmin):
    list_display = [field.name for field in TCoreUserDetail._meta.fields]