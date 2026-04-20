# producer/main.py
import json
import logging
from typing import Dict, Any
from kafka import KafkaProducer # type: ignore
from config import KAFKA_BROKER, TOPIC_NAME
from fetcher import start_streaming

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger("ProducerMain")

producer = KafkaProducer(
    bootstrap_servers=[KAFKA_BROKER],
    api_version=(0, 11, 5),
    value_serializer=lambda v: json.dumps(v).encode('utf-8'),
    retries=5
)

def send_to_broker(data: Dict[str, Any]) -> None:
    # Use logger instead of print
    logger.info(f"Streaming: {data['symbol']} @ ₹{data['price_inr']:,.2f} | Vol: ₹{data['volume_inr']:,.2f}")
    # Push the payload into Redpanda
    producer.send(TOPIC_NAME, value=data)

if __name__ == "__main__":
    logger.info("Starting Producer... Press Ctrl+C to stop.")
    try:
        start_streaming(callback=send_to_broker)
    except KeyboardInterrupt:
        logger.info("Producer stopped by user.")
    finally:
        producer.flush()
        producer.close()