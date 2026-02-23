
# processor/main.py
from spark_session import get_spark_session
from transformations import parse_kafka_stream
from sink import write_to_postgres
from config import KAFKA_BROKER, TOPIC_NAME

if __name__ == "__main__":
    print("🚀 Starting PySpark Streaming Processor...")
    spark = get_spark_session()
    
    # The 'failOnDataLoss' is now inside this function call
    stream_df = parse_kafka_stream(spark, KAFKA_BROKER, TOPIC_NAME)
    
    query = stream_df.writeStream \
        .foreachBatch(write_to_postgres) \
        .outputMode("update") \
        .option("checkpointLocation", "./checkpoints") \
        .start()
        
    print("⏳ Waiting for live crypto data...")
    query.awaitTermination()