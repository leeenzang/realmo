from django.shortcuts import render
from visit.models import Visitor
from datetime import datetime, timedelta
from django.db.models import Count
from .forms import DateRangeForm

def revisit_rate(request):
    if request.method == 'POST':
        form = DateRangeForm(request.POST)
        if form.is_valid():
            days = int(form.cleaned_data['duration'])
    else:
        days = 30
        form = DateRangeForm()

    end_date = datetime.now().date()
    start_date = end_date - timedelta(days=days)
    extended_start_date = end_date - timedelta(days=days*2)

    # 선택한 기간 동안의 방문 기록
    all_visits = Visitor.objects.filter(사용일__range=(start_date, end_date))

    # 선택한 기간 동안의 고유한 방문 고객
    all_unique_uids = all_visits.values_list('UID', flat=True).distinct()

    # 2배 확장된 기간 동안의 방문 기록으로 재방문 고객 수 계산
    revisited_records = Visitor.objects.filter(사용일__range=(extended_start_date, end_date)).values('UID').annotate(visit_count=Count('사용일')).filter(visit_count__gt=1, 사용일__gte=start_date)
    revisited_uids_count = revisited_records.count()

    # 재방문률 계산
    revisit_rate = (revisited_uids_count / len(all_unique_uids)) * 100 if all_unique_uids else 0
    
    context = {
        'revisit_rate': revisit_rate,
        'form': form
    }
    return render(request, 'analytics/revisit_rate.html', context)


