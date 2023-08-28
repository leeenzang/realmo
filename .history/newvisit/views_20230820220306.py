from django.shortcuts import render
from .models import DailyNewVisitors, MonthlyNewVisitors

def daily_new_visitors(request):
    daily_visitors = DailyNewVisitors.objects.all().order_by('-date')  # 최근 데이터부터 보여주기 위해
    context = {
        'daily_visitors': daily_visitors
    }
    return render(request, 'newvisit/daily_visitors.html', context)


def monthly_new_visitors(request):
    monthly_visitors = MonthlyNewVisitors.objects.all().order_by('-year', '-month')  # 최근 데이터부터
    context = {
        'monthly_visitors': monthly_visitors
    }
    return render(request, 'newvisit/monthly_visitors.html', context)
