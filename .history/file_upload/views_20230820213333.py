from django.shortcuts import render, redirect
from .models import Visitor
from .forms import UploadFileForm
from datetime import datetime, timedelta
import csv
from io import TextIOBase
from io import TextIOWrapper

# Create your views here.


def upload_csv(request):
    message = "어"  # 추가: 사용자에게 보여줄 메시지를 저장하는 변수

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

            message = "업로드가 성공적으로 완료되었습니다!"  # 성공 메시지 설정
        else:
            message = "오류가 발생했습니다. 다시 시도해주세요."

    else:
        form = UploadFileForm()

    return render(request, 'upload.html', {'form': form, 'message': message})
