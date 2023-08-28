from django.urls import path
from . import views

app_name = 'visit'

urlpatterns = [
    path('upload/', views.upload_csv, name='upload_csv'),
    path('upload_success/', views.upload_success, name='upload_success_url'),

]

