from django.shortcuts import render
from .models import CryptoAggregate, WhaleAlert

def index(request):
    # Fetch top 10 aggregates and top 5 whale alerts
    aggregates = CryptoAggregate.objects.all().order_by('-window_start')[:10]
    alerts = WhaleAlert.objects.all().order_by('-alert_timestamp')[:5]
    
    return render(request, 'tracker/index.html', {
        'aggregates': aggregates,
        'alerts': alerts
    })