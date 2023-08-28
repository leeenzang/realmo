from django.urls import path
from . import views

urlpatterns = [
    path('new/', views.new_visitors_summary, name='new_visitors'),
]
