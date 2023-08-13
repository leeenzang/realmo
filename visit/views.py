from django.shortcuts import render, redirect
from .models import Visitor
from .forms import UploadFileForm
from datetime import datetime, timedelta
import csv
from io import TextIOBase
from io import TextIOWrapper

# Create your views here.
def upload_success(request):
    return render(request, 'upload_success.html')

def upload_csv(request):
    if request.method == 'POST':
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            csv_file = TextIOWrapper(request.FILES['file'].file, encoding='utf-8')
            reader = csv.reader(csv_file)
            next(reader)  

            for row in reader:
                uid = row[1]
                datetime_str = row[12]
                date_obj = datetime.strptime(datetime_str, '%y-%m-%d %H:%M').date()

                visitor, created = Visitor.objects.get_or_create(UID=uid, 사용일=date_obj)

                if not created:
                    visitor.save()

            return redirect('visit:upload_success_url')  
    else:
        form = UploadFileForm()

    return render(request, 'upload.html', {'form': form})


def delete_old_data():
    three_months_ago = datetime.today().date() - timedelta(days=90)
    Visitor.objects.filter(사용일__lt=three_months_ago).delete()
