# producer/config.py
import os

# for good RAM and use docker directly
# KAFKA_BROKER = os.getenv("KAFKA_BROKER", "redpanda:9092")
# TOPIC_NAME = "raw_crypto_trades"


# for local host testing
KAFKA_BROKER = os.getenv("KAFKA_BROKER", "localhost:9092")
TOPIC_NAME = "raw_crypto_trades"

STREAMS = [
    "btcusdt@trade",
    "ethusdt@trade",
    "usdttry@trade" 
]

WEBSOCKET_URL = f"wss://stream.binance.com:9443/ws/{'/'.join(STREAMS)}"