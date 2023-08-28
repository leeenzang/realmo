from django.urls import path
from . import views

app_name = 'analytics'

urlpatterns = [
    path('revisit_rate/', views.revisit_rate, name='revisit_rate'),
]
