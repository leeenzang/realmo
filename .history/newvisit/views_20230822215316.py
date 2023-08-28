from django.shortcuts import render
from .models import DailyNewVisitors, MonthlyNewVisitors

def new_visitors_summary(request):
    daily_visitors = DailyNewVisitors.objects.all().order_by('-date')
    monthly_visitors = MonthlyNewVisitors.objects.all().order_by('-year', '-month')
    context = {
        'daily_visitors': daily_visitors,
        'monthly_visitors': monthly_visitors
    }
    return render(request, 'newvisit/visitors.html', context)
