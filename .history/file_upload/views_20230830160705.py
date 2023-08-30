from django.shortcuts import render, redirect
from .models import Visitor
from .forms import UploadFileForm
from datetime import datetime, timedelta, date
import csv
from io import TextIOBase
from io import TextIOWrapper
from newvisit.models import DailyNewVisitors, MonthlyNewVisitors
from django.db.models import Sum, Count
from django.db.models.functions import ExtractMonth, ExtractYear


# Create your views here.

# 일별 신규 방문자 수 갱신
def update_monthly_new_visitors(year, month):
    monthly_new_count = DailyNewVisitors.objects.filter(date__year=year, date__month=month).aggregate(Sum('new_visitors_count'))['new_visitors_count__sum'] or 0
    MonthlyNewVisitors.objects.update_or_create(year=year, month=month, defaults={'new_visitors_count': monthly_new_count})

# 월별 신규 방문자 수 갱신
def update_monthly_new_visitors():
    dates = DailyNewVisitors.objects.values_list('date', flat=True).distinct()
    for d in dates:
        year, month = d.year, d.month
        monthly_new_count = DailyNewVisitors.objects.filter(date__year=year, date__month=month).aggregate(Sum('new_visitors_count'))['new_visitors_count__sum'] or 0
        MonthlyNewVisitors.objects.update_or_create(year=year, month=month, defaults={'new_visitors_count': monthly_new_count})



# 사용자가 웹에 접근할때 호출
def upload_csv(request):
    dates_to_update = set()
    # 사용자가 폼을 통해 서버로 보냈을때 해당 요청 처리하는 코드
    if request.method == 'POST':
        form = UploadFileForm(request.POST, request.FILES)
        uploaded_filename = request.FILES['file'].name  # 파일의 이름 가져오기

        if form.is_valid():
            # 사용자가 업로드한 CSV 파일 읽고 각 행 데이터 처리해서 Visitor 모델에 저장
            csv_file = TextIOWrapper(request.FILES['file'].file, encoding='utf-8')
            reader = csv.reader(csv_file)
            next(reader)  # 헤더(첫번째 줄) 스킵

            for row in reader:
                uid = row[1]
                datetime_str = row[12]
                date_obj = datetime.strptime(datetime_str, '%y-%m-%d %H:%M').date()
                classification = row[6]  
                
                # 해당 날짜를 업데이트할 목록에 추가
                dates_to_update.add(date_obj)

                # 기존 레코드 확인 및 저장
                visitor, created = Visitor.objects.get_or_create(UID=uid, 사용일=date_obj, defaults={'uploaded_filename': uploaded_filename})
                if '신규' in classification:
                    visitor.구분 = classification
                    visitor.save()
                

            # 일별 신규 방문자 업데이트
            update_daily_new_visitors(date_obj)

            # 현재 월의 신규 방문자 업데이트
            today = datetime.today().date()
            update_monthly_new_visitors(today.year, today.month)

            message = "업로드가 성공적으로 완료되었습니다!"  # 성공 메시지 설정
        else:
            message = "오류가 발생했습니다. 다시 시도해주세요."

    # 사용자가 처음 페이지 접속했을때
    else:
        form = UploadFileForm()
        message = ""  # 여기에서 message 변수를 초기화
        uploaded_filename = ""  # POST가 아닌 경우에는 빈 문자열로 초기화

    # 일별 방문자 데이터 가져오기
    three_months_ago = date.today() - timedelta(days=90)

    # 월별 방문자 데이터 가져오기
    monthly_visitors = Visitor.objects.values(month=ExtractMonth('사용일'), year=ExtractYear('사용일')).annotate(visitors_count=Count('UID', distinct=True)).order_by('-year', '-month')

    # 이 부분에서 일별 전체 방문자 수를 계산
    daily_visitors_count = Visitor.objects.values('사용일').annotate(visitors_count=Count('UID', distinct=True)).order_by('-사용일')

    # 주어진 데이터와 함께 템플릿에 렌더링해서 사용자에게 웹 표시
    return render(request, 'file_upload/upload.html', {'form': form, 'message': message, 'daily_visitors': daily_visitors_count, 'monthly_visitors': monthly_visitors, 'uploaded_filename': uploaded_filename})
