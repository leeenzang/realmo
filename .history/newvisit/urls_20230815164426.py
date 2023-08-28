from django.urls import path
from . import views

urlpatterns = [
    path('new/', views.new_visitors, name='new_visitors'),
]
