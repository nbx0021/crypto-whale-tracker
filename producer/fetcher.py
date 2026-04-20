# producer/fetcher.py
import json
import websocket
import time
import logging
from typing import Callable, Dict, Any
from config import WEBSOCKET_URL
from fx_rate import fx_cache

logger = logging.getLogger("BinanceFetcher")

def on_message(ws: websocket.WebSocketApp, message: str, callback: Callable[[Dict[str, Any]], None]) -> None:
    data = json.loads(message)
    
    # Dynamically pull the live INR rate (Zero lag due to caching)
    current_inr_rate = fx_cache.get_usd_to_inr()
    
    # Standardizing the Binance payload to our Industry Format
    standard_data = {
        "symbol": data['s'].lower().replace('usdt', 'inr'),
        "price_inr": float(data['p']) * current_inr_rate,
        "quantity": float(data['q']),
        "volume_inr": (float(data['p']) * float(data['q'])) * current_inr_rate,
        "timestamp": data['E']
    }
    
    callback(standard_data)

def start_streaming(callback: Callable[[Dict[str, Any]], None]) -> None:
    recon_delay = 1
    max_delay = 60

    while True:
        logger.info(f"Connecting to Binance WebSocket: {WEBSOCKET_URL}")
        
        ws = websocket.WebSocketApp(
            WEBSOCKET_URL,
            on_message=lambda ws, msg: on_message(ws, msg, callback),
            on_error=lambda ws, err: logger.error(f"WebSocket Error: {err}"),
            on_close=lambda ws, close_status, close_msg: logger.warning("WebSocket Closed")
        )
        
        ws.run_forever()
        
        logger.warning(f"Connection lost. Reconnecting in {recon_delay} seconds...")
        time.sleep(recon_delay)
        recon_delay = min(recon_delay * 2, max_delay)