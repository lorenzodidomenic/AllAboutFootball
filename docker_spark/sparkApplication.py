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

from pyspark.ml.regression import LinearRegression
from pyspark.ml.feature import VectorAssembler
from pyspark.ml import Pipeline
#from pyspark.ml.evaluation import RegressionEvaluator

#creiamo lo Spark Context della nostra applicazione
#sc = SparkContext(appName="PythonStructuredStreamsKafka")
#spark = SparkSession(sc)
#sc.setLogLevel("ERROR")

spark = SparkSession.builder.appName("FootbALL").getOrCreate()
spark.sparkContext.setLogLevel("ERROR")   # To reduce verbose output


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

#df=df.selectExpr("CAST(timestamp AS STRING)","CAST(value AS STRING)") \

#df.printSchema()  
#finora lo schema è (timestamp,value) dove value contiene un json 


#definiamo lo schema del response
#questo è lo schema del mio json
schema = StructType([
    StructField("parameters",StructType([
      StructField("season",StringType(),True)
    ])),
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
    .select("data.parameters.season","data.response.league.standings.team.name","data.response.league.standings.rank",
    "data.response.league.standings.points","data.response.league.standings.all.goals.for","data.response.league.standings.all.goals.against",
    "data.response.league.standings.all.win","data.response.league.standings.all.draw","data.response.league.standings.all.lose").alias("text")\

#parseDf = df.withColumn("parsed",from_json("value",schema))

#parseDf.select("parsed.response.league.standings")

#parseDf = parseDf.filter(parseDf.name.contains('Roma')).groupBy("name").agg(F.collect_list("season").alias("season"),F.collect_list("rank").alias("rank"),F.collect_list("points").alias("points"),F.collect_list("for").alias("scored goals "),F.collect_list("against").alias("conceded_goals"))
#parseDf = parseDf.groupBy("name").agg(F.mean("rank").alias("media_rank"))

#io qua dovrei trainare il modello sulla regressione??
#train_data,test_data = parseDf.randomSplit([0.7,0.3],seed=42)

featureassembler = VectorAssembler(inputCols = ["points","for","against","win","draw","lose"],outputCol = "features") #definisco le colonne indipendneti del mio dataframe
#parseDf = featureassembler.transform(parseDf)

training = spark.createDataFrame([
  (90,98,15,33,4,1,1),
  (70,68,35,31,6,1,2),
  (63,78,25,29,6,3,3),
  (58,90,30,26,10,2,6),
  (87,90,15,26,6,6,4),
  (80,88,29,25,10,3,4),
  (59,49,20,20,10,8,8),
  (25,38,20,10,20,8,15),
  (90,70,15,31,6,1,1),
  (88,78,16,30,6,2,2)
],["points","for","against","rank","win","draw","lose"])

lr = LinearRegression(featuresCol="features",labelCol="rank",predictionCol="Predicted_rank")
pipeline = Pipeline(stages=[featureassembler,lr])
model = pipeline.fit(training)

trainingPred = model.transform(training)
#trainingPred.select('features','rank','Predicted_rank').show()

#adesso ho il mio modello (lo posso salvare e lo applico ogni volta sullo streaming?)
#prediction = model.transform(parseDf)
#prediction.show()
#posso salvare il modello in una cartella e riutilizarlo 

#pred_results = regressor.evalutate(test_data)
#pred_results.predictions.show()

#predictions = model.trasform(test_data)
#evaluator = RegressionEvaluator(labelCol='label_column',predictionCol='prediction',metricName='rmse')
#rmse = evaluator.evaluate(predictions)
#print("Root Mean Squared Error on test data: ",rmse)


#alleno il modello ogni volta che leggo nuovi dati

#coefficients = lr_model.coefficients
#intercept = lr_model.intercept

#print("Coefficitents: ",coefficients)
#print("Intercept: {:.3f}".format(intercept))


#lo manderò ad elastic search e visualizzo su kibana

predictDf = model.transform(parseDf).select('name','season','features','rank','Predicted_rank')
predictDf.writeStream \
  .outputMode("append")\
  .format('console')\
  .option('truncate', value=False) \
  .option("numRows",10000)\
  .start()\
  .awaitTermination()
