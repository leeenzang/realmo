from django.urls import path
from . import views

app_name = 'newvisit'  # <-- 이 부분 추가


urlpatterns = [
    path('new/', views.new_visitors_summary, name='new_visitors'),
]
