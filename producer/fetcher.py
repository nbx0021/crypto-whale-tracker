# producer/fetcher.py
import json
import websocket
from config import WEBSOCKET_URL
from fx_rate import fx_cache

def on_message(ws, message, callback):
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

def start_streaming(callback):
    ws = websocket.WebSocketApp(
        WEBSOCKET_URL,
        on_message=lambda ws, msg: on_message(ws, msg, callback),
        on_error=lambda ws, err: print(f"Error: {err}"),
        on_close=lambda ws, close_status, close_msg: print("### Closed ###")
    )
    print(f"Connecting to Binance WebSocket: {WEBSOCKET_URL}")
    ws.run_forever()