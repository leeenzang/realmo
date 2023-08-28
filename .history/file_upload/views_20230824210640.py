from django.shortcuts import render, redirect
from .models import Visitor
from .forms import UploadFileForm
from datetime import datetime, timedelta, date
import csv
from io import TextIOBase
from io import TextIOWrapper
from newvisit.models import DailyNewVisitors, MonthlyNewVisitors
from django.db.models import Sum


# Create your views here.


# 사용자가 웹에 접근할때 호출
def upload_csv(request):

    # 사용자가 폼을 통해 서버로 보냈을때 해당 요청 처리하는 코드
    if request.method == 'POST':
        form = UploadFileForm(request.POST, request.FILES)
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


                # 기존의 레코드를 찾습니다.
                visitor = Visitor.objects.filter(UID=uid, 사용일=date_obj).first()

                # 레코드가 없으면 새로 생성합니다.
                if not visitor:
                    visitor = Visitor(UID=uid, 사용일=date_obj)

                # '신규'가 classification에 포함되면 구분을 업데이트합니다.
                if '신규' in classification:
                    visitor.구분 = classification

                # 변경사항을 저장합니다.
                visitor.save()
                

            # 현재 날짜 및 달 계산
            today = datetime.today().date()
            
            current_month = today.month
            current_year = today.year

            # Daily update, Visitor 모델에서 신규 필터링
            daily_new_count = Visitor.objects.filter(사용일=today, 구분__in=['신규카드', '신규현금']).distinct().count()
            DailyNewVisitors.objects.update_or_create(date=today, defaults={'new_visitors_count': daily_new_count})

            # Monthly update, 데일리 이용해서 신규 수 합계 계산
            monthly_new_count = DailyNewVisitors.objects.filter(date__year=current_year, date__month=current_month).aggregate(Sum('new_visitors_count'))['new_visitors_count__sum'] or 0
            MonthlyNewVisitors.objects.update_or_create(year=current_year, month=current_month, defaults={'new_visitors_count': monthly_new_count})

            message = "업로드가 성공적으로 완료되었습니다!"  # 성공 메시지 설정
        else:
            message = "오류가 발생했습니다. 다시 시도해주세요."

    # 사용자가 처음 페이지 접속했을때
    else:
        form = UploadFileForm()
        message = ""  # 여기에서 message 변수를 초기화
    
    # 일별 방문자 데이터 가져오기
    three_months_ago = date.today() - timedelta(days=90)
    daily_visitors = DailyNewVisitors.objects.filter(date__gte=three_months_ago).order_by('-date')
    # 주어진 데이터와 함께 템플릿에 렌더링해서 사용자에게 웹 표시
    return render(request, 'file_upload/upload.html', {'form': form, 'message': message, 'daily_visitors': daily_visitors})
