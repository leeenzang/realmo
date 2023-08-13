from django.contrib import admin
from .models import Visitor

# Register your models here.

class VisitorAdmin(admin.ModelAdmin):
    list_display = ('UID', '사용일')
    list_filter = ('사용일',)
    
admin.site.register(Visitor, VisitorAdmin)