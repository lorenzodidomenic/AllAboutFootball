from __future__ import print_function

import sys

from pyspark import SparkContext
from pyspark.sql import SparkSession
from pyspark.streaming import StreamingContext
from pyspark.sql.dataframe import DataFrame

from pyspark.sql.functions import *

from pyspark.sql.types import *


#creiamo lo Spark Context della nostra applicazione
sc = SparkContext(appName="PythonStructuredStreamsKafka")
spark = SparkSession(sc)
sc.setLogLevel("ERROR")

kafkaServer="kafkaServer:9092"
topic = "topicCountries"

# Streaming Query

#mi leggo lo stream da kafka
df = spark \
  .readStream \
  .format("kafka") \
  .option("kafka.bootstrap.servers", kafkaServer) \
  .option("subscribe", topic) \
  .load()

df=df.selectExpr("CAST(timestamp AS STRING)","CAST(value AS STRING)") \

df.printSchema()  
#finora lo schema è (timestamp,value) dove value contiene un json 


#definiamo lo schema delresponse
#questo è lo schema del mio json
schema = StructType([
    StructField("response",StructType([
    StructField("league",StructType([
      StructField("standings",StructType([
          StructField("points",IntegerType(),True),
          StructField("all",StructType([
          StructField("played",IntegerType(),True),
          StructField("win",IntegerType(),True),
          StructField("lose",IntegerType(),True),
          StructField("draw",IntegerType(),True),
          StructField("goals",StructType([
            StructField("against",IntegerType(),True),
            StructField("for",IntegerType(),True)
         ])),
         ])),
          StructField("rank",IntegerType(),True),
          StructField("team",StructType([
          StructField("name",StringType(),True)
         ])
         )])
      )])
    )])
  )])


parseDf = df.selectExpr("CAST(value AS STRING)") \
    .select(from_json("value", schema).alias("data")) \
    .select("data.response.league.standings.team.name","data.response.league.standings.rank",
    "data.response.league.standings.points","data.response.league.standings.all.goals.for","data.response.league.standings.all.goals.against",
    "data.response.league.standings.all.win","data.response.league.standings.all.draw","data.response.league.standings.all.lose").alias("text")#, col("data.content").alias("text"))

#parseDf = df.withColumn("parsed",from_json("value",schema))

#parseDf.select("parsed.response.league.standings")

parseDf.writeStream \
  .outputMode("Append")\
  .format('console')\
  .option('truncate', 'false')\
  .start()\
  .awaitTermination()
