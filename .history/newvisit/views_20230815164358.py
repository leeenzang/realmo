from django.shortcuts import render
from visit.models import calculate_new_visitors

def new_visitors(request):
    new_visitors_count = calculate_new_visitors()
    return render(request, 'newvisit/new_visitors.html', {'new_visitors': new_visitors_count})
