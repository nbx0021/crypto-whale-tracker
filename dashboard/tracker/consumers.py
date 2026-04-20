import json
import asyncio
import logging
from typing import Dict, Any
from channels.generic.websocket import AsyncWebsocketConsumer # type: ignore
from channels.db import database_sync_to_async # type: ignore
import datetime
from django.utils import timezone
from .models import CryptoAggregate, WhaleAlert

logger = logging.getLogger("DashboardConsumer")

class DashboardConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        await self.accept()
        self.keep_polling = True
        # Start the background loop when a user connects
        asyncio.create_task(self.send_live_data())
        logger.info("WebSocket connected.")

    async def disconnect(self, close_code):
        self.keep_polling = False
        logger.info("WebSocket disconnected.")

    @database_sync_to_async
    def get_dashboard_data(self) -> Dict[str, Any]:
        # Fetch Data (latest first)
        aggs_qs = CryptoAggregate.objects.all().order_by('-window_start')[:15].values(
            'symbol', 'window_start', 'avg_price_inr', 'total_volume_inr', 'trade_count'
        )
        aggs = list(aggs_qs)
        
        alerts = list(WhaleAlert.objects.all().order_by('-alert_timestamp')[:8].values(
            'symbol', 'alert_timestamp', 'trade_price_inr', 'trade_volume_inr', 'volume_multiplier'
        ))
        
        # Reverse the aggregations so the oldest of the 15 is first, making it perfect for charting
        aggs.reverse()
        
        # Format dates and decimals so they can be sent as JSON
        for agg in aggs:
            # Handle naive datetimes from DB
            dt = agg['window_start']
            if timezone.is_naive(dt):
                dt = timezone.make_aware(dt, datetime.timezone.utc)
            
            local_time = timezone.localtime(dt)
            agg['window_start_label'] = local_time.strftime('%H:%M')
            agg['window_start'] = local_time.strftime('%Y-%m-%d %H:%M:%S')
            agg['avg_price_inr'] = float(agg['avg_price_inr'])
            agg['total_volume_inr'] = float(agg['total_volume_inr'])
            
        for alert in alerts:
            adt = alert['alert_timestamp']
            if timezone.is_naive(adt):
                adt = timezone.make_aware(adt, datetime.timezone.utc)
                
            local_alert_time = timezone.localtime(adt)
            alert['alert_timestamp'] = local_alert_time.strftime('%H:%M:%S')
            alert['trade_price_inr'] = float(alert['trade_price_inr'])
            alert['trade_volume_inr'] = float(alert['trade_volume_inr'])
            alert['volume_multiplier'] = float(alert['volume_multiplier'])
            
        # We also want to provide the chart series data directly for ease of use in the frontend
        # Let's group chart data by symbol, though for simplicity we will just return the array
        # of dicts and let the frontend filter by the symbol it cares about (e.g. btcinr)
            
        return {'aggregates': aggs, 'alerts': alerts}

    async def send_live_data(self):
        while self.keep_polling:
            try:
                data = await self.get_dashboard_data()
                # Push data to frontend
                await self.send(text_data=json.dumps(data))
            except Exception as e:
                logger.error(f"Error fetching/sending data: {e}")
            # Wait 2 seconds before checking the database again
            await asyncio.sleep(2)