from __future__ import print_function

import sys
import numpy

from pyspark import SparkContext
from pyspark.sql import SparkSession
from pyspark.streaming import StreamingContext
from pyspark.sql.dataframe import DataFrame
from pyspark.sql.functions import *
from pyspark.sql.types import *
from pyspark.sql import functions as F
from pyspark.sql.functions import udf

from pyspark.ml.regression import LinearRegression
from pyspark.ml.feature import VectorAssembler
from pyspark.ml import Pipeline
from pyspark.ml.pipeline import PipelineModel
#from pyspark.ml.evaluation import RegressionEvaluator

from pyspark.conf import SparkConf



elastic_index = "football"
sparkConf = SparkConf().set("es.nodes","elasticsearch")\
                     .set("es.port","9200")


spark = SparkSession.builder.appName("FootbALL").config(conf=sparkConf).getOrCreate()
spark.sparkContext.setLogLevel("ERROR")   


kafkaServer="kafkaServer:9092"
topic = "topicSerieA"
modelPath = "/tmp/footbAllVolume/Completemodel"   #path dove ho salvato il mio modello, in un volume condiviso montato sul container


#mi leggo lo stream da kafka
df = spark \
  .readStream \
  .format("kafka") \
  .option("kafka.bootstrap.servers", kafkaServer) \
  .option("failOnDataLoss", False)\
  .option("subscribe", topic) \
  .load()


#definiamo lo schema del response
#questo è lo schema del mio json
schema = StructType([
    StructField("parameters",StructType([
      StructField("season",StringType(),True)
    ])),
    StructField("@timestamp",StringType(),True),
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

#il value json lo trasformiamo con quello schema e prendiamo le colonne
parseDf = df.selectExpr("CAST(value AS STRING)") \
    .select(from_json("value", schema).alias("data")) \
    .select("data.parameters.season","data.@timestamp","data.response.league.standings.team.name","data.response.league.standings.rank",
    "data.response.league.standings.points","data.response.league.standings.all.goals.for","data.response.league.standings.all.goals.against",
    "data.response.league.standings.all.win","data.response.league.standings.all.draw","data.response.league.standings.all.lose").alias("text")\


model = PipelineModel.load(modelPath)  #carico il modello


#user defined function per evitare che mi vengano predette posizioni inferiori allo 0 o superiori alla 20 esima 
def map_(x):
    if x <= 1: 
      x =1.0 
    elif x >= 20:
      x= 20.0
    else:
      x=x
    return x

map_udf = udf(map_,FloatType())    #la trasformo in udf function


predictDf = model.transform(parseDf).select('@timestamp','name','season','rank','Predicted_rank',"for","against","win","draw","lose")
predictDf = predictDf.withColumn("Predicted_rank",map_udf("Predicted_rank"))


#mando ad elastic
predictDf.writeStream \
   .option("checkpointLocation", "/tmp/") \
   .format("es") \
   .start(elastic_index) \
   .awaitTermination()

spark.stop()