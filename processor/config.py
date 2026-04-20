import os

# Use environment variables for Docker compatibility
KAFKA_BROKER = os.getenv("KAFKA_BROKER", "redpanda:29092")
TOPIC_NAME = os.getenv("TOPIC_NAME", "raw_crypto_trades")

DB_HOST = os.getenv("DB_HOST", "postgres")
DB_PORT = os.getenv("DB_PORT", "5432")
DB_NAME = os.getenv("DB_NAME", "crypto_streaming")
DB_USER = os.getenv("DB_USER", "admin")
DB_PASSWORD = os.getenv("DB_PASSWORD", "adminpassword")
DB_DRIVER = "org.postgresql.Driver"

# Construct JDBC URL dynamically
DB_URL = f"jdbc:postgresql://{DB_HOST}:{DB_PORT}/{DB_NAME}?options=-c%20timezone=Asia/Kolkata"

# The "Whale" threshold
WHALE_VOLUME_THRESHOLD = int(os.getenv("WHALE_THRESHOLD", 180000))
