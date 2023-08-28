from django.contrib import admin
from .models import DailyNewVisitors, MonthlyNewVisitors

# Register your models here.

class NewVisitorAdmin(admin.ModelAdmin):
    list_display = ('UID', '사용일','구분')
    list_filter = ('사용일',)
    
