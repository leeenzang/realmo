from django.shortcuts import render
from visit.models import Visitor
from datetime import datetime, timedelta
from django.db.models import Count

def revisit_rate(request):
    end_date = datetime.now().date()
    start_date = end_date - timedelta(days=30)

    # 30일 이내 방문 기록
    all_visits = Visitor.objects.filter(사용일__range=(start_date, end_date))
    
    # 30일 이내 고유한 방문 고객
    all_unique_uids = all_visits.values_list('UID', flat=True).distinct()

    # 30일 이내 2번 이상 방문한 고객
    revisited_uids = all_visits.values('UID').annotate(visit_count=Count('사용일')).filter(visit_count__gt=1).values_list('UID', flat=True)

    # 재방문률 계산
    revisit_rate = (len(revisited_uids) / len(all_unique_uids)) * 100 if all_unique_uids else 0
    
    context = {
        'revisit_rate': revisit_rate
    }
    return render(request, 'analytics/revisit_rate.html', context)



def analytics_home(request):
    return render(request, 'analytics/home.html')
