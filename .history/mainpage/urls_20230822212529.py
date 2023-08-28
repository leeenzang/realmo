from django.urls import path
from .views import home

app_name = 'newvisit'  # <-- 이 부분 추가


urlpatterns = [
    path('', home, name='home'),
]
