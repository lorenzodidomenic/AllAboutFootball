from __future__ import print_function

import sys

from pyspark import SparkContext
from pyspark.sql import SparkSession
from pyspark.streaming import StreamingContext
from pyspark.sql.dataframe import DataFrame

from pyspark.sql.functions import *

sc = SparkContext(appName="PythonStructuredStreamsKafka")
spark = SparkSession(sc)
sc.setLogLevel("ERROR")

kafkaServer="kafkaServer:9092"
topic = "topicCountries"

# Streaming Query

df = spark \
  .readStream \
  .format("kafka") \
  .option("kafka.bootstrap.servers", kafkaServer) \
  .option("subscribe", topic) \
  .load()

df=df.selectExpr("CAST(timestamp AS STRING)","CAST(value AS STRING)") \

df.printSchema()

df.writeStream \
  .outputMode("Append")\
  .format('console')\
  .option('truncate', 'false')\
  .start()\
  .awaitTermination()
