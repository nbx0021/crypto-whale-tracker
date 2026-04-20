# 🐋 Crypto Whale Tracker Pro

<div align="center">

![Python](https://img.shields.io/badge/Python_3.11-3776AB?style=for-the-badge&logo=python&logoColor=white)
![Apache Spark](https://img.shields.io/badge/Apache%20Spark_3.4-E25A1C?style=for-the-badge&logo=apachespark&logoColor=white)
![Docker](https://img.shields.io/badge/Docker-2496ED?style=for-the-badge&logo=docker&logoColor=white)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL_15-316192?style=for-the-badge&logo=postgresql&logoColor=white)
![Django](https://img.shields.io/badge/Django_Channels-092E20?style=for-the-badge&logo=django&logoColor=white)
![Redpanda](https://img.shields.io/badge/Redpanda_(Kafka)-E50695?style=for-the-badge&logo=apachekafka&logoColor=white)

**An industry-grade, distributed streaming pipeline that ingests live cryptocurrency trades from Binance, detects massive "Whale" volume anomalies using PySpark Structured Streaming, and visualizes results in real-time via a glassmorphic dark-mode dashboard.**

[View on Docker Hub](#-docker-hub-images) · [Local Setup](#-hybrid-local-setup-recommended-for-4gb-ram) · [Docker Setup](#-standard-containerized-setup-8gb-ram)

</div>

---

## 📸 Live Dashboard Preview

![Whale Tracker Pro Dashboard](dashboard/static/images/whale%20tracker.png)
> *Live view showing the BTC/INR 1-Minute Tumbling Window chart, Whale Anomaly alerts panel, and the Global Market Stream data table — all updating via WebSockets in real time.*

---

## 📖 Overview

**Crypto Whale Tracker Pro** monitors live trade streams from the **Binance WebSocket API** for BTC/INR, ETH/INR, and INR/TRY pairs. Every trade is published to a **Redpanda (Kafka-compatible)** message broker. A **PySpark Structured Streaming** engine consumes these events, applies 60-second micro-batch aggregations, flags anomalously large trades (Whales) exceeding a configurable INR threshold, and persists results into **PostgreSQL**. A **Django Channels ASGI** server then pushes this data to a premium glassmorphic dashboard via WebSockets — delivering sub-second latency visualization.

---

## 🏗️ System Architecture

```
┌─────────────────────────────────────────────────────────────────────┐
│                         DATA FLOW                                   │
│                                                                     │
│  Binance WebSocket API                                              │
│  (BTC/ETH/USDT Live Trades)                                         │
│          │                                                          │
│          ▼                                                          │
│  ┌───────────────┐     JSON events    ┌────────────────────────┐   │
│  │ Python        │ ────────────────► │ Redpanda               │   │
│  │ Producer      │                   │ (Kafka-compatible       │   │
│  │ (WebSocket +  │                   │  Message Broker)        │   │
│  │  FX Caching)  │                   │  Topic: raw_crypto_     │   │
│  └───────────────┘                   │        trades           │   │
│                                      └──────────┬─────────────┘   │
│                                                 │                  │
│                                                 ▼                  │
│                                      ┌────────────────────────┐   │
│                                      │ PySpark Structured     │   │
│                                      │ Streaming Engine       │   │
│                                      │                        │   │
│                                      │  • 60s micro-batches   │   │
│                                      │  • Whale detection     │   │
│                                      │    (volume > ₹1.8L)    │   │
│                                      │  • Aggregations        │   │
│                                      └──────────┬─────────────┘   │
│                                                 │                  │
│                                                 ▼                  │
│                                      ┌────────────────────────┐   │
│                                      │ PostgreSQL 15          │   │
│                                      │                        │   │
│                                      │  • crypto_aggregates   │   │
│                                      │  • whale_alerts        │   │
│                                      └──────────┬─────────────┘   │
│                                                 │                  │
│                                                 ▼                  │
│                                      ┌────────────────────────┐   │
│                                      │ Django Channels        │   │
│                                      │ (ASGI + WebSocket)     │   │
│                                      │                        │   │
│                                      │  Pushes to browser     │   │
│                                      │  every 2 seconds       │   │
│                                      └──────────┬─────────────┘   │
│                                                 │                  │
│                                                 ▼                  │
│                                      ┌────────────────────────┐   │
│                                      │  Live Dashboard        │   │
│                                      │  (ApexCharts +         │   │
│                                      │   TailwindCSS)         │   │
│                                      │  localhost:8000        │   │
│                                      └────────────────────────┘   │
└─────────────────────────────────────────────────────────────────────┘
```

---

## 🧩 Component Breakdown

| Component | Technology | Role |
|---|---|---|
| **Producer** | Python 3.11, `websocket-client`, `kafka-python` | Streams live trade events from Binance and publishes to Redpanda with FX rate caching |
| **Message Broker** | Redpanda v23.2 (Kafka-compatible) | High-throughput, fault-tolerant event buffer decoupling ingestion from processing |
| **Stream Processor** | PySpark 3.4 Structured Streaming | Consumes events in 60s microbatches, computes rolling aggregations, detects whale anomalies |
| **Data Store** | PostgreSQL 15 | Persists aggregation metrics and whale alert records with indexed time-series queries |
| **Backend / API** | Django 4.x + Django Channels (Daphne/ASGI) | Async WebSocket server that polls the DB and pushes live data to all connected clients |
| **Frontend** | HTML5, TailwindCSS, ApexCharts, Vanilla JS | Glassmorphic dark-mode dashboard with real-time chart, alerts panel, and data table |

---

## 🛠️ Tech Stack

- **Language:** Python 3.11
- **Stream Processing:** Apache Spark 3.4.1 (PySpark Structured Streaming)
- **Message Broker:** Redpanda v23.2.1 (Kafka-compatible, zero-ZooKeeper)
- **Database:** PostgreSQL 15
- **Web Framework:** Django 4.x + Django Channels 4.x (Daphne ASGI server)
- **Frontend:** TailwindCSS, ApexCharts.js
- **Containerization:** Docker & Docker Compose
- **Data Source:** Binance WebSocket Trade Streams

---

## 📋 Prerequisites

### For Containerized (Docker) Setup
- [Docker Desktop](https://www.docker.com/products/docker-desktop/) (v20+)
- **8 GB+ RAM** recommended for all services

### For Hybrid (Local) Setup
- Python 3.11+
- Java 11+ (required for PySpark)
- [Docker Desktop](https://www.docker.com/products/docker-desktop/) (for Redpanda & PostgreSQL infrastructure)
- **4 GB+ RAM** is sufficient

---

## 🚀 Standard Containerized Setup (8GB+ RAM)

This launches the **entire pipeline** — broker, database, producer, processor, and dashboard — as Docker containers.

### Step 1: Clone the Repository

```bash
git clone https://github.com/nbx0021/crypto-whale-tracker.git
cd crypto_whale_tracker
```

### Step 2: Configure Environment

Copy the example environment file and review defaults:

```bash
cp .env.example .env
```

Key variables in `.env`:

```env
# Database
DB_NAME=crypto_streaming
DB_USER=admin
DB_PASSWORD=adminpassword
DB_HOST=127.0.0.1
DB_PORT=5433

# Kafka / Redpanda
KAFKA_BROKER=localhost:9092
TOPIC_NAME=raw_crypto_trades

# Whale Detection Threshold (in INR)
WHALE_THRESHOLD=180000
```

### Step 3: Build and Launch All Services

```bash
docker-compose up -d --build
```

This starts 5 services in the correct dependency order:

```
redpanda-broker  →  crypto-db  →  whale-producer
                              →  whale-processor
                              →  whale-dashboard
```

### Step 4: Initialize the Database Schema

Run the Django migration to create all required tables:

```bash
docker exec whale-dashboard python manage.py makemigrations tracker
docker exec whale-dashboard python manage.py migrate
```

### Step 5: Access the Dashboard

Open your browser at:

```
http://localhost:8000
```

> ⏳ Wait approximately **60 seconds** for the first PySpark micro-batch to complete and populate the charts.

---

## 🪫 Hybrid Local Setup (Recommended for 4GB RAM)

Apache Spark is memory-intensive. This approach runs only the lightweight infrastructure (Redpanda + PostgreSQL) in Docker, while the producer, processor, and dashboard run as local Python processes — dramatically reducing RAM usage.

### Step 1: Start Core Infrastructure Only

```bash
docker-compose up -d redpanda postgres
```

Verify both are healthy:

```bash
docker ps
```

You should see `(healthy)` next to both `redpanda-broker` and `crypto-db`.

### Step 2: Set Up Python Virtual Environment

```bash
# Create and activate virtual environment
python -m venv venv

# Windows
venv\Scripts\activate

# macOS / Linux
source venv/bin/activate
```

### Step 3: Install Dependencies

```bash
# Dashboard dependencies
pip install -r dashboard/requirements.txt

# Producer dependencies
pip install -r producer/requirements.txt

# Processor dependencies (installs PySpark)
pip install -r processor/requirements.txt
```

### Step 4: Configure for Local Connections

The `.env` file is already pre-configured for local connections:

```env
DB_HOST=127.0.0.1
DB_PORT=5433
KAFKA_BROKER=localhost:9092
```

Verify `processor/config.py` uses the correct local JDBC URL:

```python
DB_URL = "jdbc:postgresql://127.0.0.1:5433/crypto_streaming"
```

### Step 5: Initialize the Database Schema

```bash
cd dashboard
python manage.py makemigrations tracker
python manage.py migrate
cd ..
```

### Step 6: Launch Services in Three Terminals

Open **3 separate terminal windows** in the project root, with your `venv` activated in each.

**Terminal 1 — Django Dashboard:**
```bash
cd dashboard
python manage.py runserver
```

**Terminal 2 — Binance Producer:**
```bash
python producer/main.py
```

**Terminal 3 — PySpark Processor:**
```bash
# Clear stale checkpoints first (important after config changes)
Remove-Item -Recurse -Force processor/checkpoints   # Windows PowerShell
# rm -rf processor/checkpoints                       # macOS / Linux

python processor/main.py
```

### Step 7: Access the Dashboard

```
http://127.0.0.1:8000
```

> ⏳ Wait approximately **60 seconds** for the first Spark batch to complete.

---

## 🐳 Docker Hub Images

Pre-built images are available on Docker Hub for direct deployment without building from source:

| Service | Image | Pull Command |
|---|---|---|
| Dashboard | `nbx0021/whale-dashboard:latest` | `docker pull nbx0021/whale-dashboard:latest` |
| Processor | `nbx0021/whale-processor:latest` | `docker pull nbx0021/whale-processor:latest` |
| Producer | `nbx0021/whale-producer:latest` | `docker pull nbx0021/whale-producer:latest` |

To use pre-built images, update `docker-compose.yml` to replace `build:` with `image:` for each service:

```yaml
# Example for dashboard service
dashboard:
  image: nbx0021/whale-dashboard:latest   # instead of build: ./dashboard
  container_name: whale-dashboard
  ports:
    - "8000:8000"
  ...
```

---

## 🗄️ Database Schema

Two tables are created by the init script and Django migrations:

### `crypto_aggregates`
Stores 1-minute batch aggregations per symbol.

| Column | Type | Description |
|---|---|---|
| `id` | SERIAL PK | Auto-increment primary key |
| `symbol` | VARCHAR(20) | e.g. `btcinr`, `ethinr` |
| `window_start` | TIMESTAMP | Start of the aggregation window |
| `window_end` | TIMESTAMP | End of the aggregation window |
| `avg_price_inr` | NUMERIC(18,2) | Average trade price in INR |
| `total_volume_inr` | NUMERIC(18,2) | Total volume traded in INR |
| `trade_count` | INT | Number of trades in the window |
| `created_at` | TIMESTAMP | Record insertion time |

### `whale_alerts`
Stores individual trades that exceeded the whale volume threshold.

| Column | Type | Description |
|---|---|---|
| `id` | SERIAL PK | Auto-increment primary key |
| `symbol` | VARCHAR(20) | Trading pair symbol |
| `alert_timestamp` | TIMESTAMP | Time of the whale trade |
| `trade_price_inr` | NUMERIC(18,2) | Price at execution in INR |
| `trade_volume_inr` | NUMERIC(18,2) | Volume of the whale trade in INR |
| `volume_multiplier` | NUMERIC(5,2) | How many × the threshold this trade was |
| `is_acknowledged` | BOOLEAN | For future alert management |
| `created_at` | TIMESTAMP | Record insertion time |

---

## ⚙️ Configuration Reference

### Environment Variables (`.env`)

| Variable | Default | Description |
|---|---|---|
| `DB_NAME` | `crypto_streaming` | PostgreSQL database name |
| `DB_USER` | `admin` | PostgreSQL username |
| `DB_PASSWORD` | `adminpassword` | PostgreSQL password |
| `DB_HOST` | `127.0.0.1` | DB host (`postgres` for full Docker) |
| `DB_PORT` | `5433` | DB port (`5432` for full Docker internal) |
| `KAFKA_BROKER` | `localhost:9092` | Redpanda broker address |
| `TOPIC_NAME` | `raw_crypto_trades` | Kafka topic name |
| `WHALE_THRESHOLD` | `180000` | Whale detection threshold in INR (₹1.8L) |
| `PYSPARK_PYTHON` | `python` | Python executable for Spark workers |
| `DEBUG` | `True` | Django debug mode |
| `SECRET_KEY` | *(placeholder)* | Django secret key — **change in production** |

### Whale Threshold Tuning

The whale detection threshold defaults to **₹1,80,000** (~$2,100 USD). Adjust in `.env`:

```env
WHALE_THRESHOLD=500000   # ₹5 Lakhs — catches only very large trades
WHALE_THRESHOLD=50000    # ₹50k — more sensitive, higher alert volume
```

---

## 🔧 Useful Commands

### View Live Logs

```bash
# All services
docker-compose logs -f

# Individual service
docker logs -f whale-producer
docker logs -f whale-processor
docker logs -f whale-dashboard
```

### Inspect the Database

```bash
# Connect to PostgreSQL
docker exec crypto-db psql -U admin -d crypto_streaming

# Quick stats
docker exec crypto-db psql -U admin -d crypto_streaming -c "SELECT COUNT(*) FROM crypto_aggregates;"
docker exec crypto-db psql -U admin -d crypto_streaming -c "SELECT COUNT(*) FROM whale_alerts;"

# Most recent aggregations
docker exec crypto-db psql -U admin -d crypto_streaming \
  -c "SELECT symbol, window_start, total_volume_inr FROM crypto_aggregates ORDER BY window_start DESC LIMIT 10;"
```

### Stop and Remove All Services

```bash
# Stop containers (preserves database volume)
docker-compose stop

# Stop and remove containers + network (preserves database volume)
docker-compose down

# Full teardown including the database volume (⚠️ deletes all data)
docker-compose down -v
```

### Reset Spark Checkpoints

Required whenever you change the Kafka broker address or Spark schema:

```bash
# PowerShell
Remove-Item -Recurse -Force processor/checkpoints

# Bash
rm -rf processor/checkpoints
```

---

## 🐛 Troubleshooting

### Dashboard is Blank / No Data

1.  **Check dashboard logs for WebSocket errors:**
    ```bash
    docker logs --tail 50 whale-dashboard
    ```
2.  **Verify the processor is writing to the DB:**
    ```bash
    docker exec crypto-db psql -U admin -d crypto_streaming -c "SELECT COUNT(*) FROM crypto_aggregates;"
    ```
    The count should be increasing every minute.
3.  **Ensure migrations have run:**
    ```bash
    docker exec whale-dashboard python manage.py migrate
    ```

### PySpark Cannot Connect to Redpanda

This happens when using hardcoded `localhost:9092` inside a Docker container. Ensure `processor/config.py` uses the Docker service name:

```python
KAFKA_BROKER = os.getenv("KAFKA_BROKER", "redpanda:29092")
```

### Out-of-Memory (OOM) Crashes

Spark requires at least **2-3 GB of RAM** to operate stably. If you encounter OOM errors:
- Switch to the [Hybrid Local Setup](#-hybrid-local-setup-recommended-for-4gb-ram)
- Or reduce Spark memory in `processor/spark_session.py`:
  ```python
  .config("spark.driver.memory", "512m")
  .config("spark.executor.memory", "512m")
  ```

### Redpanda Not Starting

Redpanda requires `--smp 1` on low-core systems. Verify the command in `docker-compose.yml` includes `--smp 1` and `--memory 1G`.

---

## 📁 Project Structure

```
crypto_whale_tracker/
│
├── producer/                  # Binance WebSocket producer
│   ├── main.py                # Entry point: KafkaProducer + stream starter
│   ├── fetcher.py             # WebSocket connection + exponential backoff
│   ├── fx_rate.py             # USD-to-INR FX rate with TTL caching
│   ├── config.py              # Broker and stream configuration
│   └── Dockerfile
│
├── processor/                 # PySpark streaming engine
│   ├── main.py                # Entry point: stream query orchestrator
│   ├── spark_session.py       # SparkSession builder with IST timezone
│   ├── transformations.py     # Schema, Kafka reader, field parsing
│   ├── sink.py                # Whale detection + PostgreSQL JDBC writer
│   ├── config.py              # DB URL, broker, and threshold config
│   └── Dockerfile
│
├── dashboard/                 # Django Channels ASGI web server
│   ├── core/
│   │   ├── settings.py        # Django settings (IST timezone, DB config)
│   │   ├── asgi.py            # ASGI + Channels router
│   │   └── urls.py
│   ├── tracker/
│   │   ├── consumers.py       # WebSocket consumer (DB poll → push)
│   │   ├── models.py          # Django ORM models (managed=False)
│   │   ├── routing.py         # WebSocket URL patterns
│   │   └── views.py           # HTTP view (serves index.html)
│   ├── templates/tracker/
│   │   └── index.html         # Full dashboard UI (Tailwind + ApexCharts)
│   ├── static/images/
│   │   └── whale tracker.png  # Dashboard screenshot
│   ├── requirements.txt
│   └── Dockerfile
│
├── database/
│   └── init.sql               # PostgreSQL table and index definitions
│
├── docker-compose.yml         # Full stack orchestration
├── .env                       # Runtime environment variables
├── .env.example               # Template for environment setup
└── README.md
```

---

## 🔄 Data Flow — Step by Step

1.  **Producer** opens a WebSocket connection to `wss://stream.binance.com` and subscribes to `btcusdt@trade`, `ethusdt@trade`, and `usdttry@trade` streams.
2.  For each incoming trade event, the producer fetches the current **USD→INR FX rate** (cached with a 5-minute TTL to avoid rate limits) and computes the INR-denominated price and volume.
3.  The normalized JSON payload is published to the `raw_crypto_trades` topic on **Redpanda**.
4.  **PySpark** continuously reads from Redpanda using the Kafka source connector, parsing the JSON messages according to a fixed schema.
5.  Every micro-batch (~60 seconds), Spark:
    - Filters trades where `volume_inr > WHALE_THRESHOLD` → writes to `whale_alerts`
    - Groups remaining trades by symbol → computes `avg_price_inr`, `total_volume_inr`, `trade_count` → writes to `crypto_aggregates`
6.  **Django Channels** runs an async background task per connected WebSocket client. Every 2 seconds, it queries the last 15 aggregation records and last 8 whale alerts, converts timestamps to **IST**, and broadcasts a JSON payload to the browser.
7.  JavaScript in the browser receives the payload, updates the **ApexCharts** area chart for BTC/INR, populates the **Whale Alerts** sidebar, and refreshes the **Global Market Stream** data table.

---

## 📜 License

This project is licensed under the **MIT License**. See [LICENSE](LICENSE) for details.

---

## 👤 Author

**Narendra Bhandari**
- GitHub: [@nbx0021](https://github.com/nbx0021)
- Docker Hub: [hub.docker.com/u/nbx0021](https://hub.docker.com/u/nbx0021)