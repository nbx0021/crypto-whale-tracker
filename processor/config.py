# processor/config.py
import os
# processor/config.py
# if you good RAM
# KAFKA_BROKER = "redpanda:9092"
# TOPIC_NAME = "raw_crypto_trades"

KAFKA_BROKER = "localhost:9092"
TOPIC_NAME = "raw_crypto_trades"

# CHANGE LOCALHOST TO 127.0.0.1
# Use the direct IP to avoid Windows "localhost" routing bugs
# Change 5432 to 5433
# processor/config.py
# Add ?options=-c%20timezone=UTC to the end of the URL
DB_URL = "jdbc:postgresql://127.0.0.1:5433/crypto_streaming?options=-c%20timezone=UTC"
# DB_URL = "jdbc:postgresql://127.0.0.1:5432/crypto_streaming?options=-c%20timezone=UTC" ##for docker and have good RAM above 16 GB
DB_USER = "admin"
DB_PASSWORD = "adminpassword"
DB_DRIVER = "org.postgresql.Driver"

# WHALE_VOLUME_THRESHOLD = 500

# The "Whale" threshold: Alert on any single trade over ₹50,00,000 (50 Lakhs)
WHALE_VOLUME_THRESHOLD = 180000
