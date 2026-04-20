from django.shortcuts import render
from django.http import HttpRequest, HttpResponse
from .models import CryptoAggregate, WhaleAlert

def index(request: HttpRequest) -> HttpResponse:
    # Fetch top 10 aggregates and top 5 whale alerts for initial load
    aggregates = CryptoAggregate.objects.all().order_by('-window_start')[:10]
    alerts = WhaleAlert.objects.all().order_by('-alert_timestamp')[:5]
    
    return render(request, 'tracker/index.html', {
        'aggregates': aggregates,
        'alerts': alerts
    })