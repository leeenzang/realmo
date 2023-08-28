from django.contrib import admin
from .models import Visitor

from datetime import datetime, timedelta
from django.contrib.admin import SimpleListFilter
# Register your models here.

class VisitorAdmin(admin.ModelAdmin):
    list_display = ('UID', '사용일','구분')
    list_filter = ('사용일',)
    
admin.site.register(Visitor, VisitorAdmin)