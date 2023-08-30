from django.contrib import admin
from .models import Visitor

from datetime import datetime, timedelta
from django.contrib.admin import SimpleListFilter
from rangefilter.filter import DateRangeFilter
from django.utils.translation import gettext_lazy as _


class NewVisitorFilter(SimpleListFilter):
    title = _('신규')  # Dropdown title
    parameter_name = '신규'  # URL parameter name

    def lookups(self, request, model_admin):
        return (
            ('신규', _('신규만 보기')),  # This will show in dropdown menu
        )

    def queryset(self, request, queryset):
        # Actual filter
        if self.value() == '신규':
            return queryset.filter(구분__icontains='신규')

class VisitorAdmin(admin.ModelAdmin):
    list_display = ('UID', '사용일','구분')
    list_filter = (
        ('사용일', DateRangeFilter),
        NewVisitorFilter,
    )
    ordering = ['-사용일']

admin.site.register(Visitor, VisitorAdmin)