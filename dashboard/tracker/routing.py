from django.urls import path
from . import consumers

websocket_urlpatterns = [
    path('ws/live-data/', consumers.DashboardConsumer.as_asgi()),
]