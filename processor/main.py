# processor/main.py
import logging
from spark_session import get_spark_session
from transformations import parse_kafka_stream
from sink import write_to_postgres
from config import KAFKA_BROKER, TOPIC_NAME

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger("ProcessorMain")

if __name__ == "__main__":
    logger.info("🚀 Starting PySpark Streaming Processor...")
    spark = get_spark_session()
    
    stream_df = parse_kafka_stream(spark, KAFKA_BROKER, TOPIC_NAME)
    
    query = stream_df.writeStream \
        .foreachBatch(write_to_postgres) \
        .outputMode("update") \
        .option("checkpointLocation", "./checkpoints") \
        .start()
        
    logger.info("⏳ Waiting for live crypto data...")
    try:
        query.awaitTermination()
    except KeyboardInterrupt:
        logger.info("🛑 Processor stopped by user.")
    finally:
        spark.stop()