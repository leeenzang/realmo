from django.shortcuts import render, redirect
from .models import Visitor
from .forms import UploadFileForm
from datetime import datetime, timedelta
import csv
from io import TextIOBase
from io import TextIOWrapper
from newvisit.models import DailyNewVisitors, MonthlyNewVisitors
from django.db.models import Sum


# Create your views here.


def upload_csv(request):

    if request.method == 'POST':
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            # --- 기존의 CSV 처리 로직 시작 ---
            csv_file = TextIOWrapper(request.FILES['file'].file, encoding='utf-8')
            reader = csv.reader(csv_file)
            next(reader)  # 헤더(첫번째 줄) 스킵

            for row in reader:
                uid = row[1]
                datetime_str = row[12]
                date_obj = datetime.strptime(datetime_str, '%y-%m-%d %H:%M').date()

                visitor, created = Visitor.objects.get_or_create(UID=uid, 사용일=date_obj)

                if not created:
                    visitor.save()
            # --- 기존의 CSV 처리 로직 끝 ---

            # 여기서 신규 방문자 업데이트 로직 추가
            today = datetime.today().date()
            current_month = today.month
            current_year = today.year

            # Daily update
            daily_new_count = Visitor.objects.filter(사용일=today, 구분__in=['신규카드', '신규현금']).distinct().count()
            DailyNewVisitors.objects.update_or_create(date=today, defaults={'new_visitors_count': daily_new_count})

            # Monthly update
            monthly_new_count = DailyNewVisitors.objects.filter(date__year=current_year, date__month=current_month).aggregate(Sum('new_visitors_count'))['new_visitors_count__sum'] or 0
            MonthlyNewVisitors.objects.update_or_create(year=current_year, month=current_month, defaults={'new_visitors_count': monthly_new_count})

            message = "업로드가 성공적으로 완료되었습니다!"  # 성공 메시지 설정
        else:
            message = "오류가 발생했습니다. 다시 시도해주세요."

    else:
        form = UploadFileForm()
        message = ""  # 여기에서 message 변수를 초기화합니다.
        
    daily_visitors = DailyNewVisitors.objects.all().order_by('-date')  # 최근 날짜부터 정렬하여 가져옴

return render(request, 'file_upload/upload.html', {'form': form, 'message': message, 'daily_visitors': daily_visitors})
