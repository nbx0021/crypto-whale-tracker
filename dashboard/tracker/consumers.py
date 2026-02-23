import json
import asyncio
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
from .models import CryptoAggregate, WhaleAlert

class DashboardConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        await self.accept()
        self.keep_polling = True
        # Start the background loop when a user connects
        asyncio.create_task(self.send_live_data())

    async def disconnect(self, close_code):
        self.keep_polling = False

    @database_sync_to_async
    def get_dashboard_data(self):
        # Fetch Data
        aggs = list(CryptoAggregate.objects.all().order_by('-window_start')[:10].values(
            'symbol', 'window_start', 'avg_price_inr', 'total_volume_inr', 'trade_count'
        ))
        alerts = list(WhaleAlert.objects.all().order_by('-alert_timestamp')[:5].values(
            'symbol', 'alert_timestamp', 'trade_price_inr', 'trade_volume_inr'
        ))
        
        # Format dates and decimals so they can be sent as JSON
        for agg in aggs:
            agg['window_start'] = agg['window_start'].strftime('%H:%M:%S')
            agg['avg_price_inr'] = float(agg['avg_price_inr'])
            agg['total_volume_inr'] = float(agg['total_volume_inr'])
            
        for alert in alerts:
            alert['alert_timestamp'] = alert['alert_timestamp'].strftime('%H:%M:%S')
            alert['trade_price_inr'] = float(alert['trade_price_inr'])
            alert['trade_volume_inr'] = float(alert['trade_volume_inr'])
            
        return {'aggregates': aggs, 'alerts': alerts}

    async def send_live_data(self):
        while self.keep_polling:
            data = await self.get_dashboard_data()
            # Push data to frontend
            await self.send(text_data=json.dumps(data))
            # Wait 2 seconds before checking the database again
            await asyncio.sleep(2)