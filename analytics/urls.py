from django.urls import path
from . import views

app_name = 'analytics'

urlpatterns = [
    path('', views.analytics_home, name='home'),
    path('revisit_rate/', views.revisit_rate, name='revisit_rate'),
]
