FROM bitnamilegacy/spark:3.4.1
USER root
ENV PYTHONUNBUFFERED=1
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
RUN mkdir -p /app/checkpoints && chmod -R 777 /app/checkpoints
# Use the full path for main.py to be safe
CMD ["spark-submit", \
     "--packages", "org.apache.spark:spark-sql-kafka-0-10_2.12:3.4.1,org.postgresql:postgresql:42.7.2", \
     "/app/main.py"]