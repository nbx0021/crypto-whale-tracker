# producer/main.py
import json
from kafka import KafkaProducer
from config import KAFKA_BROKER, TOPIC_NAME
from fetcher import start_streaming

# Initialize Redpanda Producer
# producer = KafkaProducer(
#     bootstrap_servers=[KAFKA_BROKER],
#     value_serializer=lambda v: json.dumps(v).encode('utf-8')
# )

producer = KafkaProducer(
    bootstrap_servers=['localhost:9092'],
    api_version=(0, 11, 5),  # Add this line
    value_serializer=lambda v: json.dumps(v).encode('utf-8')
)

def send_to_broker(data):
    # Print to terminal so you can verify it's working
    print(f"Streaming: {data['symbol']} @ ₹{data['price_inr']:,.2f}")
    # Push the payload into Redpanda
    producer.send(TOPIC_NAME, value=data)

if __name__ == "__main__":
    print("Starting Producer... Press Ctrl+C to stop.")
    try:
        start_streaming(callback=send_to_broker)
    except KeyboardInterrupt:
        print("\nProducer stopped.")