from django.shortcuts import render
from .models import DailyNewVisitors, MonthlyNewVisitors

def new_visitors_summary(request):
    daily_visitors = DailyNewVisitors.objects.all().order_by('-date')
    monthly_visitors = MonthlyNewVisitors.objects.all().order_by('-year', '-month')
    
    # 월별 데이터마다 해당 월의 일별 데이터를 가져오는 코드 추가
    for monthly_visitor in monthly_visitors:
        monthly_visitor.daily_data = DailyNewVisitors.objects.filter(
            date__year=monthly_visitor.year,
            date__month=monthly_visitor.month
        ).order_by('-date')

    context = {
        'daily_visitors': daily_visitors,
        'monthly_visitors': monthly_visitors
    }
    return render(request, 'newvisit/new_visitors.html', context)
