import os
from pyspark.sql import SparkSession

# Ensure HADOOP_HOME is correct (pointing to folder ABOVE bin)
os.environ["HADOOP_HOME"] = "C:\\hadoop"

# 2. Adding the bin folder to the execution path for this script session
os.environ["PATH"] += os.pathsep + "C:\\hadoop\\bin"

def get_spark_session():
    spark = SparkSession.builder \
        .appName("CryptoWhaleTracker") \
        .config("spark.jars.packages", "org.apache.spark:spark-sql-kafka-0-10_2.12:3.4.1,org.postgresql:postgresql:42.7.2,org.apache.commons:commons-pool2:2.11.1") \
        .config("spark.sql.shuffle.partitions", "2") \
        .config("spark.driver.extraJavaOptions", "-Duser.timezone=UTC") \
        .config("spark.executor.extraJavaOptions", "-Duser.timezone=UTC") \
        .config("spark.sql.session.timeZone", "UTC") \
        .master("local[*]") \
        .getOrCreate()
        
    spark.sparkContext.setLogLevel("WARN")
    return spark