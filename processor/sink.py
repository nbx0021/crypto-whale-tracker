# processor/sink.py
from config import DB_URL, DB_USER, DB_PASSWORD, DB_DRIVER, WHALE_VOLUME_THRESHOLD
from pyspark.sql import functions as F

def write_to_postgres(batch_df, batch_id):
    if batch_df.isEmpty():
        return
        
    # ACTION 1: Filter out the "Whales" and save them to the alerts table
    whales_df = batch_df.filter(F.col("volume_inr") > WHALE_VOLUME_THRESHOLD)
    
    if not whales_df.isEmpty():
        alerts_df = whales_df.select(
            F.col("symbol"),
            F.col("trade_time").alias("alert_timestamp"),
            F.col("price_inr").alias("trade_price_inr"),
            F.col("volume_inr").alias("trade_volume_inr"),
            F.lit(0.0).alias("volume_multiplier") 
        )
        
        alerts_df.write.format("jdbc").option("url", DB_URL) \
            .option("dbtable", "whale_alerts").option("user", DB_USER) \
            .option("password", DB_PASSWORD).option("driver", DB_DRIVER) \
            .mode("append").save()

    # ACTION 2: Aggregate the 1-minute micro-batch for the dashboard
    agg_df = batch_df.groupBy("symbol").agg(
        F.min("trade_time").alias("window_start"),
        F.max("trade_time").alias("window_end"),
        F.sum("volume_inr").alias("total_volume_inr"),
        F.avg("price_inr").alias("avg_price_inr"),
        F.count("*").alias("trade_count")
    )
        
    agg_df.write.format("jdbc").option("url", DB_URL) \
        .option("dbtable", "crypto_aggregates").option("user", DB_USER) \
        .option("password", DB_PASSWORD).option("driver", DB_DRIVER) \
        .mode("append").save()