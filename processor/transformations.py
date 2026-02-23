# processor/transformations.py
from pyspark.sql import functions as F
from pyspark.sql.types import StructType, StructField, StringType, DoubleType, LongType

# 1. Define the incoming JSON schema from our Producer
SCHEMA = StructType([
    StructField("symbol", StringType(), True),
    StructField("price_inr", DoubleType(), True),
    StructField("quantity", DoubleType(), True),
    StructField("volume_inr", DoubleType(), True),
    StructField("timestamp", LongType(), True)
])

def parse_kafka_stream(spark, kafka_broker, topic_name):
    # Connect to Redpanda
    raw_stream = spark.readStream \
        .format("kafka") \
        .option("kafka.bootstrap.servers", kafka_broker) \
        .option("subscribe", topic_name) \
        .option("startingOffsets", "latest") \
        .option("failOnDataLoss", "false") \
        .load()

    # Cast Kafka byte value to String and parse JSON
    parsed_stream = raw_stream.selectExpr("CAST(value AS STRING)") \
        .select(F.from_json(F.col("value"), SCHEMA).alias("data")) \
        .select("data.*")
        
    # Convert Unix timestamp (ms) to Spark TimestampType
    return parsed_stream.withColumn("trade_time", F.from_unixtime(F.col("timestamp") / 1000).cast("timestamp"))