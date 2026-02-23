
# 🐋 Crypto Whale Tracker

![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white)
![Apache Spark](https://img.shields.io/badge/Apache%20Spark-E25A1C?style=for-the-badge&logo=Apache%20Spark&logoColor=white)
![Docker](https://img.shields.io/badge/Docker-2496ED?style=for-the-badge&logo=docker&logoColor=white)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-316192?style=for-the-badge&logo=postgresql&logoColor=white)
![Django](https://img.shields.io/badge/Django-092E20?style=for-the-badge&logo=django&logoColor=white)
![Apache Kafka](https://img.shields.io/badge/Redpanda_(Kafka)-231F20?style=for-the-badge&logo=apachekafka&logoColor=white)

## Overview
A complete, real-time data engineering pipeline that tracks cryptocurrency "whales" (massive trades). It ingests live trade data from the Binance WebSocket API, processes it through a distributed streaming engine using 1-minute tumbling windows, and pushes the aggregations and anomaly alerts to a live dashboard.

## 🏗️ System Architecture
1. **Data Ingestion (Producer):** A Python script establishes a persistent WebSocket connection to Binance, capturing real-time trades for BTC, ETH, and other assets.
2. **Message Broker (Redpanda/Kafka):** The raw trades are published to a `raw_crypto_trades` topic, acting as a high-throughput buffer to decouple ingestion from processing.
3. **Stream Processing (PySpark):** A Spark Structured Streaming application consumes the Kafka topic, calculates 1-minute windowed averages, and flags single trades exceeding a predefined volume threshold.
4. **Storage (PostgreSQL):** Processed aggregates and whale alerts are upserted into relational database tables.
5. **Visualization (Django):** A Django web server uses Django Channels (WebSockets) to stream the database updates to a live frontend UI.

## 🛠️ Technologies Used
* **Languages:** Python, SQL
* **Processing:** Apache Spark (PySpark Structured Streaming)
* **Messaging:** Redpanda (Kafka API compatible)
* **Database:** PostgreSQL
* **Web:** Django, Django Channels, HTML/JS
* **DevOps:** Docker, Docker Compose

---

## 🚀 Getting Started (Standard Containerized Setup)
*Use this setup if your machine has 8GB+ of RAM.*

1. **Clone the repository**
   ```bash
   git clone [https://github.com/yourusername/crypto_whale_tracker.git](https://github.com/yourusername/crypto_whale_tracker.git)
   cd crypto_whale_tracker

```

2. **Start the Infrastructure**
```bash
docker-compose up -d

```


3. **Initialize the Database**
```bash
docker exec -it whale-dashboard python manage.py migrate

```


4. **Access the Dashboard**
Open `http://localhost:8000` in your browser. Wait ~60 seconds for the first Spark batch to process.

---

## 🪫 Low-RAM / Hybrid Setup (For 4GB RAM Machines)

*Apache Spark and Docker are highly resource-intensive. If your system runs out of memory (yielding `java.lang.NullPointerException` crashes in Spark), use this Hybrid approach. It runs the heavy infrastructure inside Docker, but executes the Python scripts natively on your host OS to save RAM.*

### Step 1: Start ONLY the Infrastructure in Docker

Ensure your `docker-compose.yml` has a dual-listener setup for Redpanda (exposing port `9092` to `localhost`).

```bash
docker-compose up -d redpanda postgres

```

### Step 2: Update Configuration Files

Before running the scripts locally, point them to your host machine (`localhost` or `127.0.0.1`) instead of the internal Docker service names.

* **In `producer/config.py` & `processor/config.py`:**
Change `KAFKA_BROKER = "redpanda:9092"` to `KAFKA_BROKER = "localhost:9092"`
* **In `processor/config.py`:**
Change the `DB_URL` host to `127.0.0.1:5433` (or whatever external port Postgres is mapped to).
* **In `dashboard/core/settings.py`:**
Change `DATABASES['default']['HOST']` to `'127.0.0.1'` and `'PORT'` to `'5433'`.

### Step 3: Run the Services Locally

Open three separate terminal windows, activate your Python virtual environment (`venv`), and start the services in this order:

**Terminal 1 (The Dashboard):**

```bash
cd dashboard
python manage.py migrate
python manage.py runserver

```

**Terminal 2 (The Producer):**

```bash
python producer/main.py

```

**Terminal 3 (The PySpark Engine):**

```bash
# Clear old checkpoints first to avoid state conflicts
rm -rf processor/checkpoints  
python processor/main.py

```

Open `http://127.0.0.1:8000` to view the live tracker!

---