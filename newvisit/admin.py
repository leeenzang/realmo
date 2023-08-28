from django.contrib import admin
from .models import DailyNewVisitors, MonthlyNewVisitors

# Register your models here.

@admin.register(DailyNewVisitors)
class DailyNewVisitorsAdmin(admin.ModelAdmin):
    list_display = ['date', 'new_visitors_count']
    search_fields = ['date']
    list_filter = ['date']

@admin.register(MonthlyNewVisitors)
class MonthlyNewVisitorsAdmin(admin.ModelAdmin):
    list_display = ['year', 'month', 'new_visitors_count']
    search_fields = ['year', 'month']
    list_filter = ['year', 'month']
